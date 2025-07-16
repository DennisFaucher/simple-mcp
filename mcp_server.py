#!/usr/bin/env python3
"""
Simple MCP Server implementation
Provides basic math operations and file system tools
"""

import asyncio
import logging
import os
import math
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("simple-mcp-server")

@mcp.tool()
def calculate(expression: str) -> str:
    """Perform basic mathematical calculations

    Args:
        expression: Mathematical expression to evaluate (e.g., '2 + 3 * 4')
    """
    try:
        # Safe evaluation of mathematical expressions
        # Only allow basic math operations
        allowed_names = {
            k: v for k, v in math.__dict__.items()
            if not k.startswith("__")
        }
        allowed_names.update({
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
        })

        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, allowed_names)

        return f"Result: {expression} = {result}"

    except Exception as e:
        return f"Calculation error: {str(e)}"

@mcp.tool()
def list_files(directory: str = ".") -> str:
    """List files in a directory

    Args:
        directory: Directory path to list files from (defaults to current directory)
    """
    try:
        if not os.path.exists(directory):
            return f"Directory does not exist: {directory}"

        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                files.append(f"📄 {item}")
            elif os.path.isdir(item_path):
                files.append(f"📁 {item}/")

        files_list = "\n".join(sorted(files))

        return f"Files in {directory}:\n{files_list}"

    except Exception as e:
        return f"Error listing files: {str(e)}"

@mcp.tool()
def read_file(filepath: str) -> str:
    """Read contents of a text file

    Args:
        filepath: Path to the file to read
    """
    try:
        if not os.path.exists(filepath):
            return f"File does not exist: {filepath}"

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        return f"Contents of {filepath}:\n\n{content}"

    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(filepath: str, content: str) -> str:
    """Write content to a text file

    Args:
        filepath: Path to the file to write
        content: Content to write to the file
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

        return f"Successfully wrote {len(content)} characters to {filepath}"

    except Exception as e:
        return f"Error writing file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
