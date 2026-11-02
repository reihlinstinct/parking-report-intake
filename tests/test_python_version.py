"""Runtime Python-version guards on the script entry points."""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # runs the guard; no exit on a supported interpreter
    return mod


class TestPythonVersionGuard(unittest.TestCase):
    def test_guards_accept_current(self):
        load("intake_validation.py", "intake_validation_guarded")
        load("prototype.py", "prototype_guarded")

    def test_guard_rejects_old(self):
        src = (ROOT / "intake_validation.py").read_text()
        start = src.index("MIN_PYTHON")
        end = src.rindex("_check_python_version()") + len("_check_python_version()")
        old = sys.version_info
        sys.version_info = (3, 10, 9)
        try:
            with self.assertRaises(SystemExit) as cm:
                exec(src[start:end], {"_sys": sys, "sys": sys})
            self.assertIn("requires Python 3.11+", str(cm.exception))
        finally:
            sys.version_info = old


if __name__ == "__main__":
    unittest.main()
