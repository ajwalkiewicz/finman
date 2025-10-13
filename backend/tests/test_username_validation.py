#!/usr/bin/env python3
"""
Test script for username and password validation functionality.
"""

import sys

sys.path.append("./backend")

from app.password_validator import PasswordValidator
from app.schemas import UserCreate
from pydantic import ValidationError


def test_username_validation():
    print("Testing username validation...")

    # Test valid usernames
    valid_usernames = ["username", "admin_user", "TestUser", "user_name_test"]

    # Test invalid usernames
    invalid_usernames = [
        "user",  # too short
        "admin1",  # contains digit
        "user-name",  # contains hyphen
        "user name",  # contains space
        "user@",  # contains special character
        "",  # empty
    ]

    print("\nValid usernames:")
    for username in valid_usernames:
        try:
            user = UserCreate(username=username, password="TempPassword123!")
            print(f"✓ {username}")
        except ValidationError as e:
            print(f"✗ {username}: {e}")

    print("\nInvalid usernames:")
    for username in invalid_usernames:
        try:
            user = UserCreate(username=username, password="TempPassword123!")
            print(f"✗ {username} should have failed but passed")
        except ValidationError:
            print(f"✓ {username}: Correctly rejected")


def test_password_username_validation():
    print("\nTesting password cannot contain username...")

    test_cases = [
        ("validuser", "Password123!", True),  # Valid - no username in password
        ("testuser", "MyPassword123!", True),  # Valid - no username in password
        ("admin", "adminPassword123", False),  # Invalid - contains username
        ("john", "JohnSmith123!", False),  # Invalid - contains username
        ("alice", "ValidPass123!", True),  # Valid - no username
        ("bob", "myBobPass123", False),  # Invalid - contains username
    ]

    for username, password, should_be_valid in test_cases:
        try:
            is_valid, errors = PasswordValidator.validate_password(password, username)
            if should_be_valid and is_valid:
                print(f"✓ {username}/{password}: Correctly accepted")
            elif not should_be_valid and not is_valid:
                username_error = any("username" in error.lower() for error in errors)
                if username_error:
                    print(
                        f"✓ {username}/{password}: Correctly rejected (contains username)"
                    )
                else:
                    print(
                        f"? {username}/{password}: Rejected for other reasons: {errors}"
                    )
            else:
                print(
                    f"✗ {username}/{password}: Unexpected result - valid={is_valid}, expected={should_be_valid}"
                )
                if errors:
                    print(f"   Errors: {errors}")
        except Exception as e:
            print(f"✗ {username}/{password}: Exception: {e}")


def test_user_create_integration():
    print("\nTesting UserCreate schema integration...")

    test_cases = [
        ("validuser", "ValidPassword123!", True),
        ("testuser", "testuserPassword123", False),  # password contains username
        ("admin", "AdminPass123!", False),  # password contains username
        ("user", "ValidPassword123!", False),  # username too short
        ("alice_bob", "SecurePass123!", True),
    ]

    for username, password, should_be_valid in test_cases:
        try:
            user = UserCreate(username=username, password=password)
            if should_be_valid:
                print(f"✓ {username}/{password}: Correctly accepted")
            else:
                print(f"✗ {username}/{password}: Should have failed but passed")
        except ValidationError as e:
            if not should_be_valid:
                print(f"✓ {username}/{password}: Correctly rejected")
                # Print specific validation errors for debugging
                for error in e.errors():
                    print(f"   - {error['loc']}: {error['msg']}")
            else:
                print(f"✗ {username}/{password}: Should have passed but failed: {e}")


if __name__ == "__main__":
    test_username_validation()
    test_password_username_validation()
    test_user_create_integration()
