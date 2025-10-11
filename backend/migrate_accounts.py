#!/usr/bin/env python3
"""
Migration script to add owner_id to accounts table and associate existing accounts with users.
This script should be run once after updating the database schema.
"""

import sqlite3
import sys
from pathlib import Path


def migrate_accounts_database(db_path: str):
    """
    Add owner_id and label_color columns to accounts table and set default values.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if owner_id column already exists
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [column[1] for column in cursor.fetchall()]

        if "owner_id" not in columns:
            print("Adding owner_id column to accounts table...")

            # Add the owner_id column
            cursor.execute("ALTER TABLE accounts ADD COLUMN owner_id INTEGER")

            # Get the first user's ID (or create a default user if none exist)
            cursor.execute("SELECT id FROM users LIMIT 1")
            result = cursor.fetchone()

            if result:
                first_user_id = result[0]
                print(
                    f"Setting all existing accounts to be owned by user ID {first_user_id}"
                )

                # Update all existing accounts to belong to the first user
                cursor.execute(
                    "UPDATE accounts SET owner_id = ? WHERE owner_id IS NULL",
                    (first_user_id,),
                )

            else:
                print(
                    "Warning: No users found in database. You'll need to manually assign account ownership."
                )

        else:
            print("owner_id column already exists in accounts table.")

        # Check if label_color column exists
        if "label_color" not in columns:
            print("Adding label_color column to accounts table...")

            # Add the label_color column with default blue color
            cursor.execute(
                "ALTER TABLE accounts ADD COLUMN label_color VARCHAR DEFAULT '#3B82F6'"
            )

            # Update existing accounts with default color
            cursor.execute(
                "UPDATE accounts SET label_color = '#3B82F6' WHERE label_color IS NULL"
            )

            print("Added label_color column with default blue color.")
        else:
            print("label_color column already exists in accounts table.")

        # Check the current schema
        cursor.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='accounts'"
        )
        current_schema = cursor.fetchone()[0]
        print(f"Current accounts table schema: {current_schema}")

        conn.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        return False

    finally:
        if conn:
            conn.close()

    return True


def main():
    # Default database paths to try
    db_paths = ["data/finances.db", "backend/data/finances.db", "finances.db"]

    # Try to find the database file
    db_path = None
    for path in db_paths:
        if Path(path).exists():
            db_path = path
            break

    if not db_path:
        print(
            "Could not find finances.db file. Please provide the path as an argument."
        )
        print("Usage: python migrate_accounts.py [path_to_finances.db]")
        sys.exit(1)

    if len(sys.argv) > 1:
        db_path = sys.argv[1]

    print(f"Using database: {db_path}")

    if migrate_accounts_database(db_path):
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
