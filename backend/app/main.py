import logging
import os
from contextlib import asynccontextmanager
from datetime import timedelta

import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from . import auth, crud, database, schemas
from .password_validator import PasswordValidationError, PasswordValidator


# Lifespan event to create database and tables
# This function runs when the application starts and before it shuts down.
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up and setting up the database...")

    # Initialize Redis for rate limiting
    load_dotenv("/app/data/.env")
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, encoding="utf-8")
    await FastAPILimiter.init(redis_connection)

    # Create database tables
    database.create_tables()
    database.setup_database()

    # Security
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        # In production, disable docs and openapi
        app.docs_url = None
        app.redoc_url = None
        app.openapi_url = None

    yield

    await FastAPILimiter.close()
    logging.info("Shutting down...")


app = FastAPI(
    title="Finance Manager API",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[
        Depends(RateLimiter(times=100, seconds=60))
    ],  # Rate limit: 100 requests per minute
)


# Exception handler for password validation errors
@app.exception_handler(PasswordValidationError)
async def password_validation_exception_handler(
    request: Request, exc: PasswordValidationError
):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "password_validation_error",
                "message": "Password validation failed",
                "requirements": exc.messages,
            }
        },
    )


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://finman.walkiewicz.io",
        "https://finman.walkiewicz.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication endpoints
@app.get("/registration-status")
def get_registration_status():
    """Check if user registration is enabled."""
    user_registration_enabled = os.getenv("USER_REGISTRATION", "true").lower() == "true"
    return {"enabled": user_registration_enabled}


@app.get("/password-requirements")
def get_password_requirements():
    """Get password requirements for the frontend to display."""
    return {
        "min_length": PasswordValidator.MIN_LENGTH,
        "requirements": [
            f"At least {PasswordValidator.MIN_LENGTH} characters long",
            "At least one uppercase letter (A-Z)",
            "At least one lowercase letter (a-z)",
            "At least one digit (0-9)",
            f"At least one special character ({PasswordValidator.SPECIAL_CHARACTERS})",
            "Cannot be a common password",
            "Cannot contain more than 3 consecutive identical characters",
            "Cannot contain simple sequences (like '1234' or 'abcd')",
            "Cannot contain the username",
        ],
    }


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_session),
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth._ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_session)):
    # Check if user registration is disabled
    user_registration_enabled = os.getenv("USER_REGISTRATION", "true").lower() == "true"
    if not user_registration_enabled:
        raise HTTPException(
            status_code=403, detail="User registration is currently disabled"
        )

    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        return crud.create_user(db=db, user=user)
    except PasswordValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "type": "password_validation_error",
                "message": "Password does not meet security requirements",
                "requirements": e.messages,
            },
        )


# User endpoints
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: database.User = Depends(auth.get_current_user)):
    return current_user


@app.put("/users/me/password")
async def change_password(
    password_data: schemas.PasswordChange,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    """Change the current user's password."""
    try:
        # Validate new password doesn't contain username
        from .password_validator import PasswordValidator

        PasswordValidator.validate_and_raise(
            password_data.new_password, current_user.username
        )

        success = crud.change_user_password(
            db,
            current_user.id,
            password_data.current_password,
            password_data.new_password,
        )

        if not success:
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        return {"message": "Password changed successfully"}

    except PasswordValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "type": "password_validation_error",
                "message": "New password does not meet security requirements",
                "requirements": e.messages,
            },
        )


# Transaction endpoints
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    try:
        user_id = getattr(current_user, "id")
        return crud.create_transaction(db=db, transaction=transaction, user_id=user_id)
    except ValueError as e:
        if "Transaction limit reached" in str(e):
            raise HTTPException(
                status_code=403,
                detail={"type": "subscription_limit_error", "message": str(e)},
            )
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    transactions = crud.get_transactions(db, user_id=user_id, skip=skip, limit=limit)
    return transactions


@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    transaction = crud.get_transaction(
        db, transaction_id=transaction_id, user_id=user_id
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    db_transaction = crud.update_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction=transaction,
        user_id=user_id,
    )
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    db_transaction = crud.delete_transaction(
        db=db, transaction_id=transaction_id, user_id=user_id
    )
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}


# Account endpoints
@app.get("/accounts/", response_model=list[schemas.Account])
def read_accounts(
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    return crud.get_accounts(db, user_id=user_id)


@app.post("/accounts/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    try:
        user_id = getattr(current_user, "id")
        return crud.create_account(db=db, account=account, user_id=user_id)
    except ValueError as e:
        if "Account limit reached" in str(e):
            raise HTTPException(
                status_code=403,
                detail={"type": "subscription_limit_error", "message": str(e)},
            )
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int,
    account: schemas.AccountCreate,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    db_account = crud.update_account(
        db=db, account_id=account_id, account=account, user_id=user_id
    )
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.delete("/accounts/{account_id}")
def delete_account(
    account_id: int,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    db_account = crud.delete_account(db=db, account_id=account_id, user_id=user_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}


# Analytics endpoints
@app.get("/analytics/expenses", response_model=schemas.ExpenseSummary)
def get_expense_summary(
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    return crud.get_expense_summary(db, user_id=user_id)


@app.get("/analytics/accounts")
def get_account_flow(
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    user_id = getattr(current_user, "id")
    return crud.get_accounts_with_transactions(db, user_id=user_id)


# Subscription endpoints
@app.get("/subscription/", response_model=schemas.SubscriptionInfo)
def get_subscription_info(
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    """Get current user's subscription information."""
    user_id = getattr(current_user, "id")
    return crud.get_subscription_info(db, user_id=user_id)


@app.put("/subscription/", response_model=schemas.User)
def update_subscription(
    subscription_update: schemas.SubscriptionUpdate,
    db: Session = Depends(database.get_session),
    current_user: database.User = Depends(auth.get_current_user),
):
    """Update user's subscription type."""
    user_id = getattr(current_user, "id")
    updated_user = crud.update_user_subscription(
        db, user_id=user_id, subscription_type=subscription_update.subscription_type
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.get("/subscription/limits")
def get_subscription_limits():
    """Get all available subscription types and their limits."""
    return database.SUBSCRIPTION_LIMITS


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
