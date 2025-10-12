from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import database, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(database.User).filter(database.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = database.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Import here to avoid circular imports
    from . import utils

    # Create Income and Expense accounts for the new user
    utils.create_user_income_expense_accounts(db, db_user.id)

    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def change_user_password(
    db: Session, user_id: int, current_password: str, new_password: str
):
    """Change user password after verifying current password."""
    user = get_user(db, user_id)
    if not user:
        return False

    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        return False

    # Update with new password
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return True


def create_transaction(
    db: Session, transaction: schemas.TransactionCreate, user_id: int
):
    # Determine if this is an expense (not a transfer between accounts)
    is_expense = (
        "false"
        if (transaction.origin_account and transaction.destination_account)
        else "true"
    )

    db_transaction = database.Transaction(
        **transaction.dict(), is_expense=is_expense, owner_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(database.Transaction)
        .filter(database.Transaction.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_transaction(db: Session, transaction_id: int, user_id: int):
    return (
        db.query(database.Transaction)
        .filter(
            database.Transaction.id == transaction_id,
            database.Transaction.owner_id == user_id,
        )
        .first()
    )


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    user_id: int,
):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if db_transaction:
        # Determine if this is an expense
        is_expense = (
            "false"
            if (transaction.origin_account and transaction.destination_account)
            else "true"
        )

        for key, value in transaction.dict().items():
            setattr(db_transaction, key, value)
        db_transaction.is_expense = is_expense
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction


def get_accounts(db: Session, user_id: int):
    return db.query(database.Account).filter(database.Account.owner_id == user_id).all()


def create_account(db: Session, account: schemas.AccountCreate, user_id: int):
    db_account = database.Account(**account.dict(), owner_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_account(db: Session, account_id: int, user_id: int):
    return (
        db.query(database.Account)
        .filter(database.Account.id == account_id, database.Account.owner_id == user_id)
        .first()
    )


def update_account(
    db: Session, account_id: int, account: schemas.AccountCreate, user_id: int
):
    db_account = get_account(db, account_id, user_id)
    if db_account:
        for key, value in account.dict().items():
            setattr(db_account, key, value)
        db.commit()
        db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: int, user_id: int):
    db_account = get_account(db, account_id, user_id)
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account


def get_expense_summary(db: Session, user_id: int):
    transactions = (
        db.query(database.Transaction)
        .filter(database.Transaction.owner_id == user_id)
        .all()
    )

    summary = {
        "total_income_pln": 0,
        "total_income_eur": 0,
        "total_income_usd": 0,
        "total_income_gtq": 0,
        "total_expense_pln": 0,
        "total_expense_eur": 0,
        "total_expense_usd": 0,
        "total_expense_gtq": 0,
        "by_category": {},
    }

    for transaction in transactions:
        currency_lower = transaction.currency.lower()
        origin = getattr(transaction, "origin_account", None)
        destination = getattr(transaction, "destination_account", None)

        # Categorize as income or expense
        if origin == "Income":
            # Money coming from Income account is income
            income_key = f"total_income_{currency_lower}"
            if income_key in summary:
                summary[income_key] += transaction.amount
        elif destination == "Expense":
            # Money going to Expense account is expense
            expense_key = f"total_expense_{currency_lower}"
            if expense_key in summary:
                summary[expense_key] += transaction.amount

        # Group by title as category for expenses only
        if destination == "Expense":
            if transaction.title not in summary["by_category"]:
                summary["by_category"][transaction.title] = 0
            summary["by_category"][transaction.title] += transaction.amount

    return summary


def get_accounts_with_transactions(db: Session, user_id: int):
    """Get all accounts with their transaction flow"""
    transactions = get_transactions(db, user_id)
    accounts = {}

    for transaction in transactions:
        origin = getattr(transaction, "origin_account", None)
        destination = getattr(transaction, "destination_account", None)

        if origin:
            if origin not in accounts:
                accounts[origin] = {"outgoing": 0, "incoming": 0}
            accounts[origin]["outgoing"] += transaction.amount

        if destination:
            if destination not in accounts:
                accounts[destination] = {"outgoing": 0, "incoming": 0}
            accounts[destination]["incoming"] += transaction.amount

    return accounts
