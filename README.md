# mcp-server

Simple MCP Server using FastMCP 2.0 with Streamable HTTP protocol running in Docker.

## Features

- **One Tool**: `add` - Adds two numbers together
- **One Resource**: `info://greeting` - Returns a welcome message

## Quick Start

### Build the Docker image

```bash
docker build -t mcp-server .
```

### Run the container

```bash
docker run -p 8000:8000 mcp-server
```

The server will be available at `http://localhost:8000/mcp`.

## Development

### Install dependencies locally

```bash
pip install -r requirements.txt
```

### Run the server locally

```bash
python server.py
```

## API

### Tool: add

Adds two integers together.

**Parameters:**
- `a` (int): First number to add
- `b` (int): Second number to add

**Returns:** The sum of the two numbers

### Resource: info://greeting

Returns a friendly welcome message.

## License

Apache License 2.0
