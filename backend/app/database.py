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

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/finances.db"

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
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    account_type = Column(String)  # bank, card, wallet, etc.
    base_currency = Column(
        String, default="PLN"
    )  # Default base currency for the account
    created_at = Column(DateTime, default=datetime.utcnow)


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


def setup_database():
    create_tables()
