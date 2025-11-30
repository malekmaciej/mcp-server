# mcp-server
Simple HTTP MCP Server

## Features

This MCP server provides:

### Tools
- **add(a, b)**: Adds two numbers together
- **validate_password(password)**: Validates password strength against security requirements

### Resources
- **info://greeting**: Returns a welcome message
- **info://password-requirements**: Returns the password security policy

## Password Requirements

Passwords must meet the following security requirements:
- Minimum 12 characters long
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character
- At least 5 unique characters
- No common weak patterns or dictionary words

Example of a **rejected** password: `Prostehaslo123` (too simple, common pattern)

## Usage

```bash
docker build -t mcp-server .
docker run -p 8000:8000 mcp-server
```

Server available at `http://localhost:8000/mcp`
