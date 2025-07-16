#!/usr/bin/env python3
"""
Simple MCP Client implementation
Connects to MCP server and demonstrates tool usage
"""

import asyncio
import logging
import json
import sys
from typing import Any, Dict, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleMCPClient:
    def __init__(self):
        self.tools = []

    async def run_with_server(self, server_command: List[str], operation: str):
        """Run client operations with server connection"""
        try:
            # Create server parameters for stdio connection
            server_params = StdioServerParameters(
                command=server_command[0],
                args=server_command[1:] if len(server_command) > 1 else []
            )

            print(f"Connecting to server with command: {' '.join(server_command)}")

            # Use async context managers properly
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()

                    logger.info("Successfully connected to MCP server")

                    # List available tools
                    await self.list_tools(session)

                    # Execute the requested operation
                    if operation == "demo":
                        await self.run_demo(session)
                    elif operation == "interactive":
                        await self.interactive_session(session)

        except Exception as e:
            logger.error(f"Client error: {e}")
            raise

    async def list_tools(self, session: ClientSession):
        """List available tools from server"""
        try:
            result = await session.list_tools()
            self.tools = result.tools

            print("\n=== Available Tools ===")
            for tool in self.tools:
                print(f"• {tool.name}: {tool.description}")
            print()

        except Exception as e:
            logger.error(f"Failed to list tools: {e}")

    async def call_tool(self, session: ClientSession, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the server"""
        try:
            result = await session.call_tool(tool_name, arguments)

            # Extract text content from result
            if result.content:
                for content in result.content:
                    if hasattr(content, 'text'):
                        return content.text

            return "No content returned"

        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return f"Error: {str(e)}"

    def parse_command_args(self, command_line: str) -> List[str]:
        """Parse command line arguments, handling quoted strings"""
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None

        i = 0
        while i < len(command_line):
            char = command_line[i]

            if not in_quotes:
                if char in ['"', "'"]:
                    in_quotes = True
                    quote_char = char
                elif char == ' ':
                    if current_arg:
                        args.append(current_arg)
                        current_arg = ""
                else:
                    current_arg += char
            else:  # in_quotes
                if char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current_arg += char

            i += 1

        # Add the last argument if there is one
        if current_arg:
            args.append(current_arg)

        return args

    async def interactive_session(self, session: ClientSession):
        """Run interactive session with the server"""
        print("\n=== Interactive MCP Client Session ===")
        print("Type 'help' for available commands, 'quit' to exit")

        while True:
            try:
                command = input("\nmcp> ").strip()

                if command.lower() in ['quit', 'exit', 'q']:
                    break
                elif command.lower() == 'help':
                    await self.show_help()
                elif command.lower() == 'tools':
                    await self.list_tools(session)
                elif command.startswith('calc '):
                    expression = command[5:].strip()
                    if expression:
                        result = await self.call_tool(session, "calculate", {"expression": expression})
                        print(f"Result: {result}")
                    else:
                        print("Usage: calc <expression>")
                elif command.startswith('ls'):
                    parts = command.split()
                    directory = parts[1] if len(parts) > 1 else "."
                    result = await self.call_tool(session, "list_files", {"directory": directory})
                    print(result)
                elif command.startswith('read '):
                    filepath = command[5:].strip()
                    if filepath:
                        result = await self.call_tool(session, "read_file", {"filepath": filepath})
                        print(result)
                    else:
                        print("Usage: read <filepath>")
                elif command.startswith('write '):
                    # Parse the write command using proper argument parsing
                    args = self.parse_command_args(command[6:].strip())

                    if len(args) >= 2:
                        filepath = args[0]
                        # Join all remaining args as content (in case content has spaces)
                        content = ' '.join(args[1:])

                        result = await self.call_tool(session, "write_file", {
                            "filepath": filepath,
                            "content": content
                        })
                        print(result)
                    else:
                        print("Usage: write <filepath> <content>")
                        print("       write <filepath> \"<content with spaces>\"")
                elif command == "":
                    continue
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")

    async def show_help(self):
        """Show help information"""
        print("\n=== Available Commands ===")
        print("help              - Show this help message")
        print("tools             - List available tools")
        print("calc <expr>       - Calculate mathematical expression")
        print("ls [directory]    - List files in directory")
        print("read <filepath>   - Read file contents")
        print("write <file> <content> - Write content to file (use quotes for content with spaces)")
        print("                        - Example: write hello.txt \"Hello, World!\"")
        print("quit              - Exit the client")
        print()

    async def run_demo(self, session: ClientSession):
        """Run a demonstration of the client capabilities"""
        print("\n=== MCP Client Demo ===")

        # Demo calculations
        print("\n1. Mathematical calculations:")
        expressions = ["2 + 3 * 4", "sqrt(16)", "pi * 2", "sin(pi/2)"]
        for expr in expressions:
            result = await self.call_tool(session, "calculate", {"expression": expr})
            print(f"  {expr} = {result}")

        # Demo file operations
        print("\n2. File operations:")

        # List current directory
        result = await self.call_tool(session, "list_files", {"directory": "."})
        print(f"  Current directory contents:\n  {result}")

        # Write a test file
        test_content = "Hello from MCP Client!\nThis is a test file."
        result = await self.call_tool(session, "write_file", {
            "filepath": "test_file.txt",
            "content": test_content
        })
        print(f"  Write result: {result}")

        # Read the test file
        result = await self.call_tool(session, "read_file", {"filepath": "test_file.txt"})
        print(f"  Read result: {result}")

        print("\nDemo completed!")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <mode> [server_command...]")
        print("Modes:")
        print("  demo                    - Run demonstration")
        print("  interactive             - Interactive session")
        print("  server <command>        - Specify server command")
        print("\nExample:")
        print("  python mcp_client.py demo")
        print("  python mcp_client.py interactive")
        print("  python mcp_client.py server python mcp_server.py")
        return

    mode = sys.argv[1]

    # Default server command
    server_command = ["python", "mcp_server.py"]

    if mode == "server" and len(sys.argv) > 2:
        server_command = sys.argv[2:]

    client = SimpleMCPClient()

    if mode == "demo":
        await client.run_with_server(server_command, "demo")
    elif mode == "interactive":
        await client.run_with_server(server_command, "interactive")
    else:
        print(f"Unknown mode: {mode}")
        return

if __name__ == "__main__":
    asyncio.run(main())
