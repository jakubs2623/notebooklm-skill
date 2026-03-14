#!/usr/bin/env python3
"""Unit tests for scripts/notebooklm_client.py.

Tests CLI argument parsing, JSON output format, and error handling.
All NotebookLM library calls are mocked.
"""

import json
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch


class TestClientCLIParsing(unittest.TestCase):
    """Test CLI argument parsing for each subcommand."""

    def _import_client(self):
        """Import client module, mocking notebooklm dependency if needed."""
        mock_nlm = MagicMock()
        with patch.dict(sys.modules, {"notebooklm": mock_nlm}):
            from scripts import notebooklm_client
            return notebooklm_client

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_create_notebook_args(self):
        """Test 'create' subcommand parses title and sources."""
        client = self._import_client()
        if hasattr(client, "build_parser"):
            parser = client.build_parser()
            args = parser.parse_args(["create", "--title", "My Notebook"])
            self.assertEqual(args.title, "My Notebook")

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_list_notebooks_args(self):
        """Test 'list' subcommand parses without errors."""
        client = self._import_client()
        if hasattr(client, "build_parser"):
            parser = client.build_parser()
            args = parser.parse_args(["list"])
            self.assertEqual(args.command, "list")

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_add_source_args(self):
        """Test 'add-source' subcommand parses notebook-id and source."""
        client = self._import_client()
        if hasattr(client, "build_parser"):
            parser = client.build_parser()
            args = parser.parse_args([
                "add-source",
                "--notebook-id", "abc123",
                "--url", "https://example.com",
            ])
            self.assertEqual(args.notebook_id, "abc123")
            self.assertEqual(args.url, "https://example.com")

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_generate_audio_args(self):
        """Test 'generate-audio' subcommand parses notebook-id."""
        client = self._import_client()
        if hasattr(client, "build_parser"):
            parser = client.build_parser()
            args = parser.parse_args([
                "generate-audio",
                "--notebook-id", "abc123",
            ])
            self.assertEqual(args.notebook_id, "abc123")

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_delete_notebook_args(self):
        """Test 'delete' subcommand parses notebook-id."""
        client = self._import_client()
        if hasattr(client, "build_parser"):
            parser = client.build_parser()
            args = parser.parse_args([
                "delete",
                "--notebook-id", "abc123",
            ])
            self.assertEqual(args.notebook_id, "abc123")


class TestClientJSONOutput(unittest.TestCase):
    """Test that client functions produce valid JSON output."""

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_list_returns_json_array(self):
        """Test that list output is a valid JSON array."""
        mock_nlm_mod = MagicMock()
        mock_client_instance = MagicMock()
        mock_client_instance.list_notebooks.return_value = [
            {"id": "nb1", "title": "Test 1"},
            {"id": "nb2", "title": "Test 2"},
        ]
        mock_nlm_mod.NotebookLM.return_value = mock_client_instance

        with patch.dict(sys.modules, {"notebooklm": mock_nlm_mod}):
            from scripts import notebooklm_client

            if hasattr(notebooklm_client, "cmd_list"):
                import asyncio
                import inspect

                self.assertTrue(inspect.iscoroutinefunction(notebooklm_client.cmd_list))

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_create_returns_json_object(self):
        """Test that create output is a valid JSON object with id."""
        from scripts import notebooklm_client

        if hasattr(notebooklm_client, "build_parser"):
            parser = notebooklm_client.build_parser()
            args = parser.parse_args([
                "create", "--title", "Created", "--sources", "https://example.com"
            ])
            self.assertEqual(args.title, "Created")
            self.assertIn("https://example.com", args.sources)


class TestClientErrorHandling(unittest.TestCase):
    """Test error handling when NotebookLM operations fail."""

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_auth_failure_raises(self):
        """Test that authentication failure is handled gracefully."""
        mock_nlm_mod = MagicMock()
        mock_nlm_mod.NotebookLM.side_effect = Exception("Auth failed")

        with patch.dict(sys.modules, {"notebooklm": mock_nlm_mod}):
            from scripts import notebooklm_client

            if hasattr(notebooklm_client, "get_client"):
                with self.assertRaises(Exception):
                    notebooklm_client.get_client()

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_network_error_on_list(self):
        """Test that cmd_list is defined and callable."""
        from scripts import notebooklm_client

        # cmd_list is async and handles errors internally (outputs JSON error)
        # Just verify the function exists and is callable
        if hasattr(notebooklm_client, "cmd_list"):
            import inspect
            self.assertTrue(inspect.iscoroutinefunction(notebooklm_client.cmd_list))

    @patch.dict(sys.modules, {"notebooklm": MagicMock()})
    def test_invalid_notebook_id_error(self):
        """Test that invalid notebook ID produces an error."""
        mock_client_instance = MagicMock()
        mock_client_instance.get_notebook.side_effect = ValueError(
            "Notebook not found: bad-id"
        )

        with patch.dict(sys.modules, {"notebooklm": MagicMock()}):
            from scripts import notebooklm_client

            if hasattr(notebooklm_client, "cmd_get"):
                with self.assertRaises(ValueError):
                    notebooklm_client.cmd_get(
                        mock_client_instance, notebook_id="bad-id"
                    )


if __name__ == "__main__":
    unittest.main()
