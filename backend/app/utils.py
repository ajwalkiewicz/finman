import csv

from sqlalchemy.orm import Session

from . import crud, schemas


def import_csv_data(db: Session, csv_file_path: str, user_id: int):
    """Import data from CSV file into the database"""

    # Create Income and Expense accounts for this user if they don't exist
    create_user_income_expense_accounts(db, user_id)
    accounts_created = {"Income", "Expense"}

    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Extract and clean data
            title = row["Title"].strip()
            origin = row["Origin"].strip() if row["Origin"].strip() != "-" else None
            destination = (
                row["Destination"].strip()
                if row["Destination"].strip() != "-"
                else None
            )
            amount_str = row["Amount"].replace(",", ".").strip()
            day_of_month = int(row["Day of Month"])
            description = row["Description"].strip()

            # Parse amount and currency
            amount_parts = amount_str.split()
            if len(amount_parts) >= 2:
                amount = float(amount_parts[0])
                currency = amount_parts[1]
            else:
                # Handle cases where currency might be missing
                amount = float(amount_str)
                currency = "PLN"  # Default currency

            # Map origin and destination to Income/Expense for household accounting
            # If origin is "Income", this represents money coming into the household
            # If destination is "Expense", this represents money leaving the household
            if origin == "Income":
                # Money from external source into household accounts
                origin_account = "Income"
                destination_account = destination
            elif destination == "Expense":
                # Money from household accounts to external expenses
                origin_account = origin
                destination_account = "Expense"
            else:
                # Transfer between household accounts
                origin_account = origin
                destination_account = destination

            # Create accounts if they don't exist (excluding Income/Expense which are already created)
            for account_name in [origin_account, destination_account]:
                if (
                    account_name
                    and account_name not in accounts_created
                    and account_name not in ["Income", "Expense"]
                ):
                    # Check if account already exists
                    existing_accounts = crud.get_accounts(db, user_id)
                    if not any(acc.name == account_name for acc in existing_accounts):
                        account_create = schemas.AccountCreate(
                            name=account_name,
                            account_type="bank",  # Default type
                        )
                        crud.create_account(db, account_create, user_id)
                    accounts_created.add(account_name)

            # Create transaction
            transaction_create = schemas.TransactionCreate(
                title=title,
                origin_account=origin_account,
                destination_account=destination_account,
                amount=amount,
                currency=currency,
                day_of_month=day_of_month,
                description=description,
            )

            crud.create_transaction(db, transaction_create, user_id)

    print(f"Successfully imported data from {csv_file_path}")


def setup_initial_data(db: Session):
    """Set up initial data including a default user and their Income/Expense accounts"""
    # Create default user if not exists
    user = crud.get_user_by_username(db, "admin")
    if not user:
        user_create = schemas.UserCreate(username="admin", password="admin123")
        user = crud.create_user(db, user_create)
        print("Created default admin user")

        # Create Income and Expense accounts for the new user
        create_user_income_expense_accounts(db, user.id)

    return user


def create_user_income_expense_accounts(db: Session, user_id: int):
    """Create Income and Expense accounts for a specific user"""
    existing_accounts = crud.get_accounts(db, user_id)
    existing_names = {acc.name for acc in existing_accounts}

    # Create Income account if it doesn't exist
    if "Income" not in existing_names:
        income_account = schemas.AccountCreate(
            name="Income",
            account_type="virtual",
            base_currency="PLN",
            label_color="#10B981",  # Green color: bg-green-100 text-green-800 equivalent
        )
        crud.create_account(db, income_account, user_id)
        print(f"Created Income account for user {user_id}")

    # Create Expense account if it doesn't exist
    if "Expense" not in existing_names:
        expense_account = schemas.AccountCreate(
            name="Expense",
            account_type="virtual",
            base_currency="PLN",
            label_color="#EF4444",  # Red color: bg-red-100 text-red-800 equivalent
        )
        crud.create_account(db, expense_account, user_id)
        print(f"Created Expense account for user {user_id}")
