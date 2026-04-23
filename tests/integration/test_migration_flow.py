from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT_DIR = Path(__file__).resolve().parents[2]


class MigrationSmokeIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "migration-smoke.db"
        self.database_url = f"sqlite+pysqlite:///{self.database_path}"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _run_alembic(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["DATABASE_URL"] = self.database_url
        return subprocess.run(
            [sys.executable, "-m", "alembic", "-c", "services/api/alembic.ini", *args],
            cwd=ROOT_DIR,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_alembic_upgrade_head_creates_expected_tables(self) -> None:
        upgrade_result = self._run_alembic("upgrade", "head")
        self.assertEqual(
            upgrade_result.returncode,
            0,
            msg=f"alembic upgrade head failed\nSTDOUT:\n{upgrade_result.stdout}\nSTDERR:\n{upgrade_result.stderr}",
        )

        current_result = self._run_alembic("current")
        combined_current_output = f"{current_result.stdout}\n{current_result.stderr}"
        self.assertEqual(
            current_result.returncode,
            0,
            msg=f"alembic current failed\nSTDOUT:\n{current_result.stdout}\nSTDERR:\n{current_result.stderr}",
        )
        self.assertIn("20260423_000001", combined_current_output)

        with sqlite3.connect(self.database_path) as connection:
            table_names = {
                row[0]
                for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            }

        expected_tables = {
            "alembic_version",
            "projects",
            "prompt_registry",
            "analysis_runs",
            "analysis_outputs",
            "workflow_drafts",
            "render_runs",
            "run_steps",
            "output_assets",
            "audit_events",
        }
        self.assertTrue(expected_tables.issubset(table_names))
