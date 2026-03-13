#!/usr/bin/env python3
"""
NotebookLM Authentication Helper

Wraps notebooklm-py's built-in auth flow for CLI use.

Auth flow (notebooklm-py v0.3.4):
    python3 -m notebooklm login
        → Opens Chromium, user logs into Google
        → Saves session to ~/.notebooklm/storage_state.json

    NotebookLMClient.from_storage()
        → Reads ~/.notebooklm/storage_state.json

Usage:
    python auth_helper.py setup    # Run `python3 -m notebooklm login`
    python auth_helper.py verify   # Verify auth via real API call
    python auth_helper.py clear    # Remove ~/.notebooklm/ directory

Output:
    JSON to stdout for machine parsing.
    Progress messages to stderr.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STORAGE_DIR = Path.home() / ".notebooklm"
STORAGE_STATE_FILE = STORAGE_DIR / "storage_state.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_out(data: dict) -> None:
    """Print JSON to stdout."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _err(msg: str) -> None:
    """Print progress / status to stderr."""
    print(f"[auth] {msg}", file=sys.stderr)


def _json_error(message: str, code: str = "AUTH_ERROR") -> None:
    """Print JSON error to stdout and exit 1."""
    _json_out({"error": message, "code": code})
    sys.exit(1)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_setup() -> None:
    """Run notebooklm-py's built-in login flow.

    Executes `python3 -m notebooklm login` which opens a headed Chromium
    browser, lets the user sign into Google, and saves the browser session
    to ~/.notebooklm/storage_state.json.
    """
    _err("Running notebooklm-py login flow...")
    _err("A browser window will open. Please sign in to your Google account.")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "notebooklm", "login"],
            timeout=300,  # 5 minutes for user to complete login
        )
    except FileNotFoundError:
        _json_error(
            "notebooklm package not found. Install with: pip install notebooklm-py",
            "PACKAGE_NOT_FOUND",
        )
    except subprocess.TimeoutExpired:
        _json_error(
            "Login timed out after 5 minutes. Please try again.",
            "TIMEOUT",
        )
    except KeyboardInterrupt:
        _json_error("Login cancelled by user.", "CANCELLED")

    if result.returncode != 0:
        _json_error(
            f"Login process exited with code {result.returncode}. "
            "Ensure notebooklm-py is installed: pip install notebooklm-py",
            "LOGIN_FAILED",
        )

    # Verify the storage state file was created
    if not STORAGE_STATE_FILE.exists():
        _json_error(
            "Login completed but storage_state.json was not created. "
            "This may indicate a browser issue. Try again.",
            "NO_STATE_FILE",
        )

    _err("Login successful. Session saved.")
    _json_out({
        "status": "ok",
        "message": "Authentication setup complete.",
        "storage_dir": str(STORAGE_DIR),
        "storage_state_file": str(STORAGE_STATE_FILE),
    })


def cmd_verify() -> None:
    """Verify saved authentication by loading the client and listing notebooks."""

    _err("Verifying saved authentication...")

    # Check storage state file exists
    if not STORAGE_STATE_FILE.exists():
        _json_out({
            "status": "not_configured",
            "valid": False,
            "message": "No saved authentication found. Run: python auth_helper.py setup",
            "storage_dir": str(STORAGE_DIR),
        })
        return

    # Try to import notebooklm
    try:
        from notebooklm import NotebookLMClient
    except ImportError:
        _json_out({
            "status": "missing_package",
            "valid": False,
            "message": "notebooklm-py not installed. Run: pip install notebooklm-py",
            "storage_state_exists": True,
        })
        return

    # Try to load client from storage and make a real API call
    import asyncio

    async def _verify_auth() -> dict:
        try:
            async with await NotebookLMClient.from_storage() as client:
                notebooks = await client.notebooks.list()
                return {
                    "status": "ok",
                    "valid": True,
                    "message": "Authentication is valid.",
                    "notebooks_count": len(notebooks),
                    "storage_state_file": str(STORAGE_STATE_FILE),
                }
        except Exception as exc:
            return {
                "status": "invalid",
                "valid": False,
                "message": f"Authentication failed: {exc}",
                "storage_state_file": str(STORAGE_STATE_FILE),
                "suggestion": "Re-run: python auth_helper.py setup",
            }

    try:
        result = asyncio.run(_verify_auth())
    except Exception as exc:
        result = {
            "status": "error",
            "valid": False,
            "message": f"Verification error: {exc}",
            "storage_state_file": str(STORAGE_STATE_FILE),
        }

    if result["valid"]:
        _err(f"Auth valid. Found {result.get('notebooks_count', '?')} notebooks.")
    else:
        _err(f"Auth invalid: {result['message']}")

    _json_out(result)


def cmd_clear() -> None:
    """Remove the entire ~/.notebooklm/ directory and all authentication data."""

    _err("Clearing saved authentication...")

    removed = []

    if STORAGE_DIR.exists():
        # List contents before removal for reporting
        contents = list(STORAGE_DIR.iterdir())
        removed = [str(f) for f in contents]

        shutil.rmtree(STORAGE_DIR)
        removed.append(str(STORAGE_DIR))
        _err(f"Removed {STORAGE_DIR} ({len(contents)} files)")
    else:
        _err("No authentication data found.")

    _json_out({
        "status": "ok",
        "message": "Authentication data cleared.",
        "removed": removed,
    })


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="NotebookLM Authentication Helper (wraps notebooklm-py v0.3.4)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python auth_helper.py setup     # Opens browser for Google login
    python auth_helper.py verify    # Check if session is valid (makes real API call)
    python auth_helper.py clear     # Remove ~/.notebooklm/ directory

Auth flow:
    setup  → runs `python3 -m notebooklm login` → saves ~/.notebooklm/storage_state.json
    verify → loads NotebookLMClient.from_storage() → calls notebooks.list()
    clear  → removes ~/.notebooklm/ entirely
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("setup", help="Run notebooklm-py login (opens browser)")
    subparsers.add_parser("verify", help="Verify auth via real API call")
    subparsers.add_parser("clear", help="Remove all saved authentication data")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "setup": cmd_setup,
        "verify": cmd_verify,
        "clear": cmd_clear,
    }

    try:
        commands[args.command]()
    except SystemExit:
        raise
    except Exception as exc:
        _json_error(f"Unexpected error: {exc}", "UNEXPECTED_ERROR")


if __name__ == "__main__":
    main()
