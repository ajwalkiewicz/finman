import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from .password_validator import PasswordValidator


class UserBase(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username meets requirements for new accounts."""
        if not re.match(r"^[a-zA-Z0-9_]{6,}$", v):
            raise ValueError(
                "Username must be at least 6 characters long and contain only "
                "English letters (a-z, A-Z), numbers (0-9), and underscores"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str, info) -> str:
        """Validate password meets security requirements."""
        # Get username from the model data
        username = info.data.get("username", "")

        # Validate password strength
        PasswordValidator.validate_and_raise(v, username)
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


class User(BaseModel):
    username: str
    id: int
    subscription_type: str
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


class SubscriptionInfo(BaseModel):
    subscription_type: str
    max_transactions: int
    current_transactions: int
    max_accounts: int
    current_accounts: int
    subscription_name: str
    can_add_transaction: bool
    can_add_account: bool


class SubscriptionUpdate(BaseModel):
    subscription_type: str

    @field_validator("subscription_type")
    @classmethod
    def validate_subscription_type(cls, v: str) -> str:
        """Validate subscription type is valid."""
        if v not in ["free", "plus", "pro"]:
            raise ValueError("Subscription type must be one of: free, plus, pro")
        return v
