"""Runtime Python-version guards on the script entry points.

Executes ONLY the extracted guard blocks - never the scripts' top-level
code.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ("intake_validation.py", "prototype.py")


def guard_block(path: str) -> str:
    src = (ROOT / path).read_text()
    start = src.index("MIN_PYTHON")
    end = src.rindex("_check_python_version()") + len("_check_python_version()")
    return src[start:end]


class TestPythonVersionGuard(unittest.TestCase):
    def test_guards_accept_current(self):
        for script in SCRIPTS:
            exec(guard_block(script), {"_sys": sys, "sys": sys})

    def test_guard_rejects_old(self):
        old = sys.version_info
        sys.version_info = (3, 10, 9)
        try:
            for script in SCRIPTS:
                with self.assertRaises(SystemExit) as cm:
                    exec(guard_block(script), {"_sys": sys, "sys": sys})
                self.assertIn("requires Python 3.11+", str(cm.exception))
        finally:
            sys.version_info = old


if __name__ == "__main__":
    unittest.main()
