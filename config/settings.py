"""Prototype configuration values.

For Step 1 these values are local-only defaults. Future production settings
should come from environment variables or a managed secrets/configuration tool.
"""

from pathlib import Path

APP_NAME = "Blenrep NZ CSP Portal"
APP_STATUS = "Step 1 architecture skeleton only"
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "prototype.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
