"""
Password validation utilities for enforcing strong password policies.
"""

import re
from typing import List, Tuple


class PasswordValidationError(Exception):
    """Custom exception for password validation errors."""

    def __init__(self, messages: List[str]):
        self.messages = messages
        super().__init__("; ".join(messages))


class PasswordValidator:
    """
    Password validator that enforces strong password requirements.

    Requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
    - No common passwords
    - No more than 3 consecutive identical characters
    - No simple sequences (like '1234' or 'abcd')
    - Cannot contain the username
    """

    MIN_LENGTH = 8
    SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Common passwords to reject
    COMMON_PASSWORDS = {
        "password",
        "123456",
        "password123",
        "admin",
        "qwerty",
        "letmein",
        "welcome",
        "monkey",
        "1234567890",
        "abc123",
        "123456789",
        "password1",
        "iloveyou",
        "123123",
        "admin123",
        "qwerty123",
        "password12",
        "welcome123",
        "master",
        "hello",
        "login",
        "guest",
        "test",
        "user",
        "root",
        "toor",
    }

    @classmethod
    def validate_password(
        cls, password: str, username: str = ""
    ) -> Tuple[bool, List[str]]:
        """
        Validate a password against all requirements.

        Args:
            password: The password to validate
            username: The username to check against (password cannot contain username)

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check minimum length
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters long")

        # Check for uppercase letter
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")

        # Check for special character
        special_char_pattern = f"[{re.escape(cls.SPECIAL_CHARACTERS)}]"
        if not re.search(special_char_pattern, password):
            errors.append(
                f"Password must contain at least one special character ({cls.SPECIAL_CHARACTERS})"
            )

        # Check against common passwords
        if password.lower() in cls.COMMON_PASSWORDS:
            errors.append("Password is too common and easily guessable")

        # Check for repeated characters (more than 3 consecutive)
        if re.search(r"(.)\1{3,}", password):
            errors.append(
                "Password cannot contain more than 3 consecutive identical characters"
            )

        # Check for simple sequences
        if cls._contains_simple_sequence(password):
            errors.append(
                "Password cannot contain simple sequences like '1234' or 'abcd'"
            )

        # Check if password contains username
        if username and len(username) >= 3 and username.lower() in password.lower():
            errors.append("Password cannot contain the username")

        return len(errors) == 0, errors

    @classmethod
    def _contains_simple_sequence(cls, password: str) -> bool:
        """Check if password contains simple sequences."""
        password_lower = password.lower()

        # Check for ascending sequences
        sequences = [
            "0123456789",
            "abcdefghijklmnopqrstuvwxyz",
            "qwertyuiopasdfghjklzxcvbnm",  # QWERTY keyboard layout
        ]

        for sequence in sequences:
            for i in range(len(sequence) - 3):
                if sequence[i : i + 4] in password_lower:
                    return True
                # Check reverse sequences too
                if sequence[i : i + 4][::-1] in password_lower:
                    return True

        return False

    @classmethod
    def validate_and_raise(cls, password: str, username: str = "") -> None:
        """
        Validate password and raise PasswordValidationError if invalid.

        Args:
            password: The password to validate
            username: The username to check against (password cannot contain username)

        Raises:
            PasswordValidationError: If password doesn't meet requirements
        """
        is_valid, errors = cls.validate_password(password, username)
        if not is_valid:
            raise PasswordValidationError(errors)

    @classmethod
    def get_requirements_text(cls) -> str:
        """Get a human-readable description of password requirements."""
        return (
            f"Password must meet the following requirements:\n"
            f"• At least {cls.MIN_LENGTH} characters long\n"
            f"• At least one uppercase letter (A-Z)\n"
            f"• At least one lowercase letter (a-z)\n"
            f"• At least one digit (0-9)\n"
            f"• At least one special character ({cls.SPECIAL_CHARACTERS})\n"
            f"• Cannot be a common password\n"
            f"• Cannot contain more than 3 consecutive identical characters\n"
            f"• Cannot contain simple sequences (like '1234' or 'abcd')\n"
            f"• Cannot contain the username"
        )
