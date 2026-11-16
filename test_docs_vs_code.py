"""Two-way doc-vs-code check for the prototype's public function surface.

Every public function in prototype.py and intake_validation.py must be
mentioned in the docs, and every function the docs present as part of the
surface must exist in the code. Stdlib only, offline; run with
`python test_docs_vs_code.py`.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = ["prototype.py", "intake_validation.py"]
DOC_FILES = [ROOT / "README.md", ROOT / "PROTOCOL.md"]
ALLOWLIST = ROOT / ".github" / "docs-vs-code-allowlist.txt"


def allowlist():
    out = {}
    if ALLOWLIST.is_file():
        for line in ALLOWLIST.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            token, _, reason = line.partition("#")
            token = token.strip()
            if not reason.strip():
                raise AssertionError(f"allowlist entry without a reason: {line}")
            out[token] = reason.strip()
    return out


def public_functions():
    out = set()
    for name in MODULES:
        text = (ROOT / name).read_text(encoding="utf-8")
        for token in re.findall(r"(?m)^def ([a-z][a-z_0-9]*)\(", text):
            if not token.startswith("test_"):
                out.add(token)
    return out


def doc_text():
    return "\n".join(p.read_text(encoding="utf-8") for p in DOC_FILES)


def documented_functions(text):
    """Backticked snake-case tokens and call-shaped references in the docs."""
    out = set()
    for span in re.findall(r"`([^`\n]+)`", text):
        if re.fullmatch(r"[a-z][a-z_0-9]*", span):
            out.add(span)
        out.update(re.findall(r"\b([a-z][a-z_0-9]*)\(", span))
    return out


class DocsVsCodeTest(unittest.TestCase):
    def test_every_public_function_is_documented(self):
        text = doc_text()
        allowed = allowlist()
        missing = sorted(
            t for t in public_functions()
            if not re.search(rf"\b{re.escape(t)}\b", text) and t not in allowed
        )
        self.assertEqual(missing, [], f"public functions missing from docs: {missing}")

    def test_every_documented_function_exists(self):
        known = public_functions() | set(allowlist())
        stale = sorted(t for t in documented_functions(doc_text()) if t not in known)
        self.assertEqual(stale, [], f"documented functions missing from code: {stale}")

    def test_doc_scan_catches_fake_function(self):
        self.assertIn("totally_fake_function", documented_functions("`totally_fake_function()`"))
        self.assertIn("totally_fake_function", documented_functions("`totally_fake_function`"))
        self.assertIn("totally_fake_function", documented_functions("`totally_fake_function(value)`"))


if __name__ == "__main__":
    unittest.main()
