"""
Password validation module with security requirements.

This module provides password strength validation following security best practices.
Passwords like "Prostehaslo123" (SimplePassword123 in Polish) would be rejected
as they contain common patterns and dictionary words.
"""

import re
from dataclasses import dataclass


@dataclass
class PasswordValidationResult:
    """Result of password validation check."""
    is_valid: bool
    errors: list[str]
    strength_score: int  # 0-100


# Common weak password patterns and words to reject
COMMON_PATTERNS = [
    r"^[a-z]+\d+$",  # lowercase + numbers only (like "password123")
    r"^[A-Z][a-z]+\d+$",  # Capitalized word + numbers (like "Password123")
    r"^(.)\1+$",  # All same character
    r"^(012|123|234|345|456|567|678|789|890)+$",  # Sequential numbers
    r"^(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)+$",  # Sequential letters
]

# Common weak passwords and their variations
COMMON_WEAK_PASSWORDS = [
    "password", "haslo", "prostehaslo",  # "haslo" and "prostehaslo" are Polish
    "qwerty", "admin", "user", "login", "welcome",
    "letmein", "monkey", "dragon", "master", "hello",
    "pass", "test", "guest", "root", "administrator",
]

# Special characters pattern and display string
SPECIAL_CHARS_PATTERN = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]"
SPECIAL_CHARS_DISPLAY = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"


class PasswordRequirements:
    """Password security requirements configuration."""
    
    def __init__(
        self,
        min_length: int = 12,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        min_unique_chars: int = 5,
        reject_common_patterns: bool = True,
        reject_common_passwords: bool = True,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.min_unique_chars = min_unique_chars
        self.reject_common_patterns = reject_common_patterns
        self.reject_common_passwords = reject_common_passwords


def validate_password(
    password: str,
    requirements: PasswordRequirements | None = None
) -> PasswordValidationResult:
    """
    Validate a password against security requirements.
    
    Args:
        password: The password to validate
        requirements: Optional custom requirements, uses defaults if not provided
        
    Returns:
        PasswordValidationResult with validation status, errors, and strength score
    """
    if requirements is None:
        requirements = PasswordRequirements()
    
    errors: list[str] = []
    strength_score = 0
    
    # Check length
    if len(password) < requirements.min_length:
        errors.append(f"Password must be at least {requirements.min_length} characters long")
    else:
        strength_score += 20
    
    if len(password) > requirements.max_length:
        errors.append(f"Password must be no more than {requirements.max_length} characters long")
    
    # Check for uppercase
    if requirements.require_uppercase:
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        else:
            strength_score += 15
    
    # Check for lowercase
    if requirements.require_lowercase:
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        else:
            strength_score += 15
    
    # Check for digit
    if requirements.require_digit:
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")
        else:
            strength_score += 15
    
    # Check for special character
    if requirements.require_special:
        if not re.search(SPECIAL_CHARS_PATTERN, password):
            errors.append(f"Password must contain at least one special character ({SPECIAL_CHARS_DISPLAY})")
        else:
            strength_score += 15
    
    # Check unique characters
    if len(set(password)) < requirements.min_unique_chars:
        errors.append(f"Password must contain at least {requirements.min_unique_chars} unique characters")
    else:
        strength_score += 10
    
    # Check for common patterns
    if requirements.reject_common_patterns:
        for pattern in COMMON_PATTERNS:
            if re.match(pattern, password, re.IGNORECASE):
                errors.append("Password matches a common weak pattern")
                strength_score = max(0, strength_score - 20)
                break
    
    # Check for common passwords
    if requirements.reject_common_passwords:
        password_lower = password.lower()
        # Remove digits for comparison
        password_alpha = re.sub(r"\d+", "", password_lower)
        
        for weak_pwd in COMMON_WEAK_PASSWORDS:
            if weak_pwd in password_lower or weak_pwd in password_alpha:
                errors.append("Password contains a common weak password pattern")
                strength_score = max(0, strength_score - 30)
                break
    
    # Bonus points for extra length
    if len(password) >= 16:
        strength_score += 10
    
    # Cap score at 100
    strength_score = min(100, strength_score)
    
    return PasswordValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        strength_score=strength_score
    )


def get_password_strength(password: str) -> str:
    """
    Get a human-readable password strength rating.
    
    Args:
        password: The password to evaluate
        
    Returns:
        String rating: "Weak", "Fair", "Good", "Strong", or "Very Strong"
    """
    result = validate_password(password)
    score = result.strength_score
    
    if score < 30:
        return "Weak"
    elif score < 50:
        return "Fair"
    elif score < 70:
        return "Good"
    elif score < 90:
        return "Strong"
    else:
        return "Very Strong"
