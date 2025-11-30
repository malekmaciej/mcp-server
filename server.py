"""
Simple MCP Server using FastMCP 2.0 with Streamable HTTP protocol.

This server provides:
- Tool: add - adds two numbers together
- Tool: validate_password - validates password strength
- Resource: greeting - returns a welcome message
- Resource: password_requirements - returns password policy
"""

from fastmcp import FastMCP
from password_validator import (
    validate_password as _validate_password,
    get_password_strength,
    PasswordRequirements,
)

# Create an MCP server instance
mcp = FastMCP("simple-mcp-server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        The sum of the two numbers
    """
    return a + b


@mcp.tool()
def validate_password(password: str) -> dict:
    """Validate a password against security requirements.

    The password must meet the following requirements:
    - At least 12 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    - Contains at least 5 unique characters
    - Does not match common weak patterns
    - Does not contain common weak passwords

    Args:
        password: The password to validate

    Returns:
        A dictionary with:
        - is_valid: boolean indicating if password meets requirements
        - errors: list of validation error messages
        - strength: password strength rating
        - strength_score: numeric score from 0-100
    """
    result = _validate_password(password)
    strength = get_password_strength(password)
    
    return {
        "is_valid": result.is_valid,
        "errors": result.errors,
        "strength": strength,
        "strength_score": result.strength_score,
    }


@mcp.resource("info://greeting")
def get_greeting() -> str:
    """Get a welcome greeting message.

    Returns:
        A friendly welcome message
    """
    return "Welcome to the Simple MCP Server! This server provides an add tool and password validation."


@mcp.resource("info://password-requirements")
def get_password_requirements() -> str:
    """Get the password security requirements policy.

    Returns:
        A description of password requirements
    """
    requirements = PasswordRequirements()
    return f"""Password Security Requirements:

1. Minimum length: {requirements.min_length} characters
2. Maximum length: {requirements.max_length} characters
3. Must contain at least one uppercase letter (A-Z)
4. Must contain at least one lowercase letter (a-z)
5. Must contain at least one digit (0-9)
6. Must contain at least one special character (!@#$%^&*()_+-=[]{{}}|;':",./<>?`~)
7. Must contain at least {requirements.min_unique_chars} unique characters
8. Must not match common weak patterns (e.g., "password123")
9. Must not contain common weak passwords (e.g., "password", "admin", "qwerty")

Examples of REJECTED passwords:
- "Prostehaslo123" - Contains common word pattern, lacks special characters
- "Password123" - Too simple, lacks special characters
- "12345678" - Only digits, too simple

Examples of ACCEPTED passwords:
- "Tr0ub4dor&3#xyz" - Mixed case, digits, special chars, unique
- "MyS3cur3P@ssw0rd!" - Mixed case, digits, special chars, long enough
"""


if __name__ == "__main__":
    # Run the server with Streamable HTTP transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
