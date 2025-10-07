from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import os

from . import crud, database, schemas, auth, utils

# Create database tables
database.create_tables()

app = FastAPI(title="Finance Manager API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database with sample data
@app.on_event("startup")
async def startup_event():
    db = next(database.get_db())
    user = utils.setup_initial_data(db)
    
    # Import CSV data if file exists
    csv_path = "/home/walu/Git/finanses/data.csv"
    if os.path.exists(csv_path):
        # Check if data already imported
        existing_transactions = crud.get_transactions(db, user.id)
        if not existing_transactions:
            utils.import_csv_data(db, csv_path, user.id)

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# User endpoints
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: database.User = Depends(auth.get_current_user)):
    return current_user

# Transaction endpoints
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    return crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    transactions = crud.get_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    transaction = crud.get_transaction(db, transaction_id=transaction_id, user_id=current_user.id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    db_transaction = crud.update_transaction(
        db=db, transaction_id=transaction_id, transaction=transaction, user_id=current_user.id
    )
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    db_transaction = crud.delete_transaction(
        db=db, transaction_id=transaction_id, user_id=current_user.id
    )
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

# Account endpoints
@app.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(db: Session = Depends(database.get_db)):
    return crud.get_accounts(db)

@app.post("/accounts/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    return crud.create_account(db=db, account=account)

# Analytics endpoints
@app.get("/analytics/expenses", response_model=schemas.ExpenseSummary)
def get_expense_summary(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    return crud.get_expense_summary(db, user_id=current_user.id)

@app.get("/analytics/accounts")
def get_account_flow(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(auth.get_current_user)
):
    return crud.get_accounts_with_transactions(db, user_id=current_user.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)