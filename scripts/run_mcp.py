#!/usr/bin/env python
"""Run the Snowflake MCP server with warnings suppressed and env vars."""
import sys
import os
import warnings
from pathlib import Path

# Suppress all warnings before any imports
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

# Load .env file from project root
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

class StderrFilter:
    """Filter stderr to remove Pydantic deprecation warnings."""
    def __init__(self, original):
        self.original = original
    def write(self, text):
        if "PydanticDeprecatedSince20" not in text and "pydantic" not in text.lower():
            self.original.write(text)
    def flush(self):
        self.original.flush()

# Apply the filter
sys.stderr = StderrFilter(sys.stderr)

try:
    from mcp_server_snowflake.server import main

    # Get credentials from environment variables
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    role = os.getenv("SNOWFLAKE_ROLE")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    if not all([account, user, password, role, warehouse]):
        raise ValueError("Missing required Snowflake environment variables. Check .env file.")

    # Set up arguments for the server
    config_path = Path(__file__).parent / "snowflake-mcp-config.yaml"
    sys.argv = [
        "snowflake-labs-mcp",
        "--account", account,
        "--user", user,
        "--role", role,
        "--warehouse", warehouse,
        "--password", password,
        "--service-config-file", str(config_path)
    ]

    sys.exit(main())
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
