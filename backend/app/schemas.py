from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from .password_validator import PasswordValidator


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets security requirements."""
        PasswordValidator.validate_and_raise(v)
        return v


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        """Validate new password meets security requirements."""
        PasswordValidator.validate_and_raise(v)
        return v


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    title: str
    origin_account: Optional[str] = None
    destination_account: Optional[str] = None
    amount: float
    currency: str
    day_of_month: int
    description: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    is_expense: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AccountBase(BaseModel):
    name: str
    account_type: str
    base_currency: str = "PLN"  # Default base currency
    label_color: str = "#3B82F6"  # Default blue color


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ExpenseSummary(BaseModel):
    total_income_pln: float
    total_income_eur: float
    total_income_usd: float
    total_income_gtq: float
    total_expense_pln: float
    total_expense_eur: float
    total_expense_usd: float
    total_expense_gtq: float
    by_category: dict
