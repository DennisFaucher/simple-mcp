# Simple MCP Server & Client

I wanted to learn Model Context Protocol. I failed a bunch of times. Then I asked Claude for help. I finally succeeded. Thanks Claude. Claude even wrote this README bc I'm not really that smart. 🙂

Just in case this AI README is wonky,
- Run mcp-server.py in one terminal session
- Run mcp_client in another terminal
- Both need to be run from the simple-mcp folder

---

A straightforward implementation of the Model Context Protocol (MCP) in Python, featuring a server with basic mathematical and file operations, and an interactive client.

## 🚀 Features

### MCP Server
- **Mathematical Calculator**: Safe evaluation of mathematical expressions
- **File System Operations**: List, read, and write files
- **Modern FastMCP Framework**: Uses the official MCP Python SDK
- **Type-Safe**: Automatic schema generation from Python type hints

### MCP Client
- **Interactive Mode**: Command-line interface with tool discovery
- **Demo Mode**: Automated demonstration of all server capabilities
- **Smart Command Parsing**: Handles quoted strings and complex arguments
- **Session Management**: Proper async context handling

## 📋 Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## 🛠️ Installation

### Using uv (Recommended)
```bash
git clone <repository-url>
cd simple-mcp
uv add "mcp[cli]"
```

### Using pip
```bash
git clone <repository-url>
cd simple-mcp
pip install "mcp[cli]"
```

## 🎯 Quick Start

### Run the Demo
See all server capabilities in action:
```bash
uv run mcp_client.py demo
```

### Interactive Mode
Start an interactive session with the server:
```bash
uv run mcp_client.py interactive
```

## 📖 Usage

### Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `calculate` | Perform mathematical calculations | `calc 2 + 3 * 4` |
| `list_files` | List files in a directory | `ls` or `ls /path/to/dir` |
| `read_file` | Read contents of a text file | `read hello.txt` |
| `write_file` | Write content to a file | `write hello.txt "Hello, World!"` |

### Interactive Commands

```bash
mcp> help                           # Show available commands
mcp> tools                          # List server tools
mcp> calc sqrt(16) + pi             # Mathematical calculation
mcp> ls                             # List current directory
mcp> write test.txt "Hello MCP!"    # Write to file
mcp> read test.txt                  # Read file contents
mcp> quit                           # Exit client
```

### Example Session

```
$ uv run mcp_client.py interactive

=== Available Tools ===
• calculate: Perform basic mathematical calculations
• list_files: List files in a directory
• read_file: Read contents of a text file
• write_file: Write content to a text file

=== Interactive MCP Client Session ===
Type 'help' for available commands, 'quit' to exit

mcp> calc 2 + 3 * 4
Result: Result: 2 + 3 * 4 = 14

mcp> write hello.txt "Hello, World!"
Successfully wrote 13 characters to hello.txt

mcp> read hello.txt
Contents of hello.txt:

Hello, World!

mcp> ls
Files in .:
📄 hello.txt
📄 mcp_client.py
📄 mcp_server.py
```

## 🏗️ Architecture

### Server (mcp_server.py)
- Built with **FastMCP** framework for simplicity
- Tools defined using `@mcp.tool()` decorators
- Automatic input/output schema generation
- Safe mathematical expression evaluation
- Comprehensive error handling

### Client (mcp_client.py)
- Uses `ClientSession` with stdio transport
- Proper async context management
- Intelligent command parsing with quote support
- Multiple operation modes (demo, interactive)

## 🔧 Advanced Usage

### Custom Server Command
Specify a different server executable:
```bash
uv run mcp_client.py server python custom_server.py
```

### Development Mode
Test the server with MCP Inspector:
```bash
mcp dev mcp_server.py
```

### Install in Claude Desktop
```bash
mcp install mcp_server.py
```

## 🛡️ Security Features

- **Safe Math Evaluation**: Restricted built-ins prevent code injection
- **File System Limits**: Operations limited to accessible directories
- **Input Validation**: Comprehensive argument checking
- **Error Handling**: Graceful degradation on failures

## 🚀 Extending the Server

Add new tools by creating functions with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_custom_tool(param1: str, param2: int = 10) -> str:
    """Description of what the tool does
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (optional)
    """
    # Your implementation here
    return f"Processed {param1} with value {param2}"
```

The tool will automatically:
- Be discoverable by clients
- Have schema generated from type hints
- Handle parameter validation
- Support optional parameters with defaults

## 📁 Project Structure

```
simple-mcp/
├── mcp_server.py          # FastMCP server implementation
├── mcp_client.py          # Interactive MCP client
├── README.md             # This file
└── requirements.txt      # Python dependencies (if using pip)
```

## 🤝 Model Context Protocol

This implementation follows the [Model Context Protocol](https://modelcontextprotocol.io/) specification, enabling:

- **Standardized Communication**: Works with any MCP-compatible client
- **Tool Discovery**: Automatic tool listing and schema sharing
- **Type Safety**: Strong typing with automatic validation
- **Extensibility**: Easy addition of new capabilities

## 📚 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Framework](https://github.com/modelcontextprotocol/python-sdk#fastmcp)
- [Claude Desktop Integration](https://claude.ai/download)

## 🐛 Troubleshooting

### Common Issues

**Import Errors**: Ensure you have the latest MCP SDK:
```bash
pip install --upgrade "mcp[cli]"
```

**Connection Errors**: Make sure the server script path is correct:
```bash
uv run mcp_client.py server python ./mcp_server.py
```

**File Permission Errors**: Ensure the client has write permissions in the target directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with both demo and interactive modes
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for creating the Model Context Protocol
- The MCP community for tools and examples
- Contributors to the MCP Python SDK
