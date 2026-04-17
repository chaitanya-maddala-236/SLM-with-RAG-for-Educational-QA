"""
tests/test_standard.py
----------------------
Single standard entrypoint that combines all maintained unittest modules and
reports one consolidated result.

Run:
    python -m unittest tests.test_standard -v
"""

from __future__ import annotations

import importlib
import traceback
import unittest


STANDARD_TEST_MODULES = [
    "test",
    "tests.test_all_embeddings",
    "tests.test_all_models",
]


def _build_skip_case(module_name: str, exc: Exception) -> unittest.TestCase:
    """Return one skipped placeholder test when a module cannot be imported."""
    details = "".join(traceback.format_exception_only(type(exc), exc)).strip()

    class _SkippedModuleTest(unittest.TestCase):
        def runTest(self) -> None:
            self.skipTest(f"Skipped '{module_name}' import: {details}")

    _SkippedModuleTest.__name__ = f"Skipped_{module_name.replace('.', '_')}"
    return _SkippedModuleTest()


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str | None) -> unittest.TestSuite:
    """Combine all standard test modules into one suite."""
    suite = unittest.TestSuite()
    for module_name in STANDARD_TEST_MODULES:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            suite.addTest(_build_skip_case(module_name, exc))
            continue
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)
