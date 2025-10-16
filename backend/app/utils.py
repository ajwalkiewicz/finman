import csv

from sqlalchemy.orm import Session

from . import crud, schemas


def import_csv_data(db: Session, csv_file_path: str, user_id: int):
    """Import data from CSV file into the database

    Warning:
        This function is used only for development and testing purposes.
        It is not intended for production use.

    - This function assumes the CSV file has a header row with specific columns.
    - It creates "Income" and "Expense" accounts if they don't exist.
    - It maps transactions to these accounts based on the origin and destination fields.
    - It handles malformed amounts like "55,99,PLN" by extracting the numeric part.
    - It skips rows with parsing errors and continues processing the rest.
    """
    # Create Income and Expense accounts for this user if they don't exist
    create_user_income_expense_accounts(db, user_id)
    accounts_created = {"Income", "Expense"}

    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Extract and clean data
                title = row["title"].strip()
                origin = (
                    row["origin_account"].strip()
                    if row["origin_account"].strip() != "-"
                    else None
                )
                destination = (
                    row["destination_account"].strip()
                    if row["destination_account"].strip() != "-"
                    else None
                )
                amount_str = row["amount"].replace(",", ".").strip()
                currency = row["currency"].strip()
                day_of_month = int(row["day_of_month"])
                description = row["description"].strip()

                # Parse amount - handle malformed amounts like "55,99,PLN"
                if currency in amount_str:
                    # Amount contains currency, extract just the number
                    amount_str = (
                        amount_str.replace(currency, "").replace(",", ".").strip()
                    )

                amount = float(amount_str)
            except (ValueError, KeyError) as e:
                print(f"Error parsing row: {row}")
                print(f"Error details: {e}")
                continue  # Skip this row and continue with the next one

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


def create_user_income_expense_accounts(db: Session, user_id: int):
    """Create Income and Expense accounts for a specific user"""
    existing_accounts = crud.get_accounts(db, user_id)
    existing_names = {acc.name for acc in existing_accounts}

    # Create Income account if it doesn't exist (bypass limits for system accounts)
    if "Income" not in existing_names:
        income_account = schemas.AccountCreate(
            name="Income",
            account_type="virtual",
            base_currency="PLN",
            label_color="#10B981",  # Green color: bg-green-100 text-green-800 equivalent
        )
        crud.create_account(db, income_account, user_id, bypass_limits=True)
        print(f"Created Income account for user {user_id}")

    # Create Expense account if it doesn't exist (bypass limits for system accounts)
    if "Expense" not in existing_names:
        expense_account = schemas.AccountCreate(
            name="Expense",
            account_type="virtual",
            base_currency="PLN",
            label_color="#EF4444",  # Red color: bg-red-100 text-red-800 equivalent
        )
        crud.create_account(db, expense_account, user_id, bypass_limits=True)
        print(f"Created Expense account for user {user_id}")
