from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[2]
API_ROOT = ROOT_DIR / "services" / "api"

if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

import app.domain.repository as repository_module


class RepositorySingletonFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        repository_module.reset_project_repository()

    def tearDown(self) -> None:
        repository_module.reset_project_repository()

    def test_get_project_repository_builds_singleton_once_under_concurrency(self) -> None:
        build_results: list[object] = []

        def build_stub() -> object:
            time.sleep(0.1)
            instance = object()
            build_results.append(instance)
            return instance

        with patch.object(repository_module, "build_project_repository", side_effect=build_stub):
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(lambda _: repository_module.get_project_repository(), range(4)))

        self.assertEqual(len(build_results), 1)
        self.assertTrue(all(result is build_results[0] for result in results))
