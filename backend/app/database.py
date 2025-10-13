import os
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:////app/data/finance_manager.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    subscription_type = Column(String, default="free")  # free, plus, pro
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="owner")
    accounts = relationship("Account", back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    account_type = Column(String)  # bank, card, wallet, etc.
    base_currency = Column(
        String, default="PLN"
    )  # Default base currency for the account
    label_color = Column(String, default="#3B82F6")  # Default blue color
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="accounts")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    origin_account = Column(
        String, nullable=True
    )  # Can be null for income without source
    destination_account = Column(String, nullable=True)  # Can be null for expenses
    amount = Column(Float)
    currency = Column(String)  # PLN, GTQ, EUR, USD
    day_of_month = Column(Integer)  # 1-31 for cyclic transactions
    description = Column(String)
    is_expense = Column(String, default="true")  # Whether this counts as expense
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="transactions")


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


# Subscription limits configuration
SUBSCRIPTION_LIMITS = {
    "free": {"max_transactions": 10, "max_accounts": 5, "name": "Free"},
    "plus": {"max_transactions": 50, "max_accounts": 15, "name": "Plus"},
    "pro": {"max_transactions": 150, "max_accounts": 50, "name": "Pro"},
}


def get_subscription_limits(subscription_type: str) -> dict:
    """Get the limits for a specific subscription type."""
    return SUBSCRIPTION_LIMITS.get(subscription_type, SUBSCRIPTION_LIMITS["free"])


def setup_database():
    create_tables()
