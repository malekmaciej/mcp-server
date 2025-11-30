"""
Simple MCP Server using FastMCP 2.0 with Streamable HTTP protocol.

This server provides:
- One tool: add - adds two numbers together
- One resource: greeting - returns a welcome message
"""

from fastmcp import FastMCP

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


@mcp.resource("info://greeting")
def get_greeting() -> str:
    """Get a welcome greeting message.

    Returns:
        A friendly welcome message
    """
    return "Welcome to the Simple MCP Server! This server provides a simple add tool."


if __name__ == "__main__":
    # Run the server with Streamable HTTP transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
