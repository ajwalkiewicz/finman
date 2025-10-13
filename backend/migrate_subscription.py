#!/usr/bin/env python3
"""
Database migration script to add subscription_type column to existing users.
This script adds the subscription_type column with a default value of 'free' for existing users.
"""

import os
import sqlite3
from contextlib import contextmanager

# Database path configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/finance_manager.db")

# Extract the file path from the URL
if DATABASE_URL.startswith("sqlite:///"):
    DB_PATH = DATABASE_URL[10:]  # Remove "sqlite:///"
    # If it's a relative path, make it absolute from the project root
    if not DB_PATH.startswith("/"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Go up one level from backend/
        DB_PATH = os.path.join(project_root, DB_PATH)
else:
    DB_PATH = DATABASE_URL


@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return column_name in columns


def add_subscription_column():
    """Add subscription_type column to users table if it doesn't exist."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the column already exists
            if check_column_exists(cursor, "users", "subscription_type"):
                print("✓ subscription_type column already exists in users table")
                return True

            print("Adding subscription_type column to users table...")

            # Add the subscription_type column with default value 'free'
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN subscription_type VARCHAR DEFAULT 'free'
            """)

            # Update any existing NULL values to 'free'
            cursor.execute("""
                UPDATE users 
                SET subscription_type = 'free' 
                WHERE subscription_type IS NULL
            """)

            conn.commit()
            print("✓ Successfully added subscription_type column")

            # Verify the column was added
            if check_column_exists(cursor, "users", "subscription_type"):
                print("✓ Column verification passed")
                return True
            else:
                print("✗ Column verification failed")
                return False

    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def verify_users_table():
    """Verify the users table structure."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            print("\nCurrent users table structure:")
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()

            for column in columns:
                print(
                    f"  - {column[1]}: {column[2]} (nullable: {'yes' if column[3] == 0 else 'no'})"
                )

            return True

    except sqlite3.Error as e:
        print(f"✗ Error verifying table: {e}")
        return False


def main():
    """Main migration function."""
    print("🔄 Starting subscription system database migration...")
    print(f"Database path: {DB_PATH}")

    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print(f"✗ Database file not found at {DB_PATH}")
        print("Please ensure the application has created the database first.")
        return False

    # Verify current table structure
    verify_users_table()

    # Add subscription column
    success = add_subscription_column()

    if success:
        print("\n✓ Migration completed successfully!")
        verify_users_table()
        return True
    else:
        print("\n✗ Migration failed!")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
