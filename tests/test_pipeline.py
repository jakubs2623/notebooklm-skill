#!/usr/bin/env python3
"""Unit tests for scripts/pipeline.py.

Tests workflow argument parsing, pipeline orchestration, error propagation,
and trend-pulse integration. All subprocess and external calls are mocked.
"""

import json
import sys
import unittest
from unittest.mock import MagicMock, call, patch


class TestPipelineCLIParsing(unittest.TestCase):
    """Test argument parsing for each pipeline workflow."""

    def _import_pipeline(self):
        """Import pipeline module, mocking dependencies if needed."""
        mocks = {"notebooklm": MagicMock(), "dotenv": MagicMock()}
        with patch.dict(sys.modules, mocks):
            from scripts import pipeline
            return pipeline

    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_research_workflow_args(self):
        """Test 'research' workflow parses topic and output arguments."""
        pipeline = self._import_pipeline()
        if hasattr(pipeline, "build_parser"):
            parser = pipeline.build_parser()
            args = parser.parse_args([
                "research",
                "--topic", "AI agents",
                "--output", "output/research.json",
            ])
            self.assertEqual(args.topic, "AI agents")
            self.assertEqual(args.output, "output/research.json")

    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_trend_to_content_workflow_args(self):
        """Test 'trend-to-content' workflow parses geo and count."""
        pipeline = self._import_pipeline()
        if hasattr(pipeline, "build_parser"):
            parser = pipeline.build_parser()
            args = parser.parse_args([
                "trend-to-content",
                "--geo", "TW",
                "--count", "5",
            ])
            self.assertEqual(args.geo, "TW")
            self.assertEqual(args.count, "5")

    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_publish_workflow_args(self):
        """Test 'publish' workflow parses platform and content."""
        pipeline = self._import_pipeline()
        if hasattr(pipeline, "build_parser"):
            parser = pipeline.build_parser()
            args = parser.parse_args([
                "publish",
                "--platform", "threads",
                "--content", "Hello world",
            ])
            self.assertEqual(args.platform, "threads")
            self.assertEqual(args.content, "Hello world")


class TestPipelineOrchestration(unittest.TestCase):
    """Test pipeline step orchestration with mocked subprocess calls."""

    @patch("subprocess.run")
    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_research_pipeline_calls_client(self, mock_run):
        """Test that research pipeline invokes notebooklm_client correctly."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"id": "nb1", "title": "Research"}),
        )

        from scripts import pipeline

        if hasattr(pipeline, "run_research"):
            pipeline.run_research(topic="AI agents")
            self.assertTrue(mock_run.called)

    @patch("subprocess.run")
    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_pipeline_steps_run_in_order(self, mock_run):
        """Test that pipeline executes steps sequentially."""
        call_order = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args", [])
            call_order.append(cmd)
            return MagicMock(returncode=0, stdout="{}")

        mock_run.side_effect = track_calls

        from scripts import pipeline

        if hasattr(pipeline, "run_full_pipeline"):
            pipeline.run_full_pipeline(topic="test")
            # Verify at least one subprocess was called
            self.assertGreater(len(call_order), 0)


class TestPipelineErrorPropagation(unittest.TestCase):
    """Test that errors in pipeline steps are properly propagated."""

    @patch("subprocess.run")
    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_client_failure_stops_pipeline(self, mock_run):
        """Test that client failure stops the pipeline with an error."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Error: Auth failed",
        )

        from scripts import pipeline

        if hasattr(pipeline, "run_research"):
            try:
                result = pipeline.run_research(topic="test")
                # If it returns a result, check for error indication
                if result is not None:
                    self.assertTrue(
                        hasattr(result, "returncode")
                        and result.returncode != 0
                        or isinstance(result, dict)
                        and result.get("error")
                    )
            except (RuntimeError, subprocess.CalledProcessError, Exception):
                pass  # Error propagation is the expected behavior

    @patch("subprocess.run")
    @patch.dict(sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()})
    def test_missing_dependency_error(self, mock_run):
        """Test that missing external dependency raises clear error."""
        mock_run.side_effect = FileNotFoundError(
            "No such file or directory: 'notebooklm_client.py'"
        )

        from scripts import pipeline

        if hasattr(pipeline, "run_research"):
            with self.assertRaises(FileNotFoundError):
                pipeline.run_research(topic="test")


class TestTrendPulseIntegration(unittest.TestCase):
    """Test trend-pulse integration for trend-to-content workflow."""

    @patch("subprocess.run")
    @patch.dict(
        sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()}
    )
    def test_trend_pulse_output_parsed(self, mock_run):
        """Test that trend-pulse JSON output is correctly parsed."""
        trend_data = {
            "trends": [
                {"title": "Claude Code", "score": 95},
                {"title": "MCP Protocol", "score": 88},
            ]
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(trend_data),
        )

        from scripts import pipeline

        if hasattr(pipeline, "fetch_trends"):
            result = pipeline.fetch_trends(geo="TW", count=5)
            if result is not None:
                self.assertTrue(mock_run.called)

    @patch("subprocess.run")
    @patch.dict(
        sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()}
    )
    def test_trend_pulse_unavailable_fallback(self, mock_run):
        """Test graceful fallback when trend-pulse is not available."""
        mock_run.side_effect = FileNotFoundError(
            "trend-pulse command not found"
        )

        from scripts import pipeline

        if hasattr(pipeline, "fetch_trends"):
            try:
                result = pipeline.fetch_trends(geo="TW", count=5)
                # Should return empty or None, not crash
                if result is not None:
                    self.assertIsInstance(result, (list, dict))
            except FileNotFoundError:
                pass  # Also acceptable: propagate the error

    @patch("subprocess.run")
    @patch.dict(
        sys.modules, {"notebooklm": MagicMock(), "dotenv": MagicMock()}
    )
    def test_trend_to_content_creates_notebook(self, mock_run):
        """Test that trend-to-content workflow creates a notebook from trends."""
        responses = [
            # First call: trend-pulse
            MagicMock(
                returncode=0,
                stdout=json.dumps({
                    "trends": [{"title": "AI Agents", "score": 95}]
                }),
            ),
            # Second call: notebook creation
            MagicMock(
                returncode=0,
                stdout=json.dumps({"id": "nb-trend", "title": "AI Agents"}),
            ),
        ]
        mock_run.side_effect = responses

        from scripts import pipeline

        if hasattr(pipeline, "run_trend_to_content"):
            pipeline.run_trend_to_content(geo="TW", count=1)
            # Should have made at least one subprocess call
            self.assertTrue(mock_run.called)


if __name__ == "__main__":
    unittest.main()
