# Coverage baseline (#14)

Recorded 2026-11-02 against default-branch SHA
`34c84c46c1e7694849ea24601052d0cd80e19bb5` (pre-PR `main`).
Updated 2026-11-02 by the #41 follow-up: `run_summary.py` now has a unit
suite and the same enforced floor.

## Test command

```sh
coverage run --branch --source=scripts/security,scripts/ci \
  -m pytest tests/security/test_scorecard_guard.py \
      tests/ci/test_run_summary.py -q
coverage report --include=scripts/security/scorecard_guard.py --fail-under=80
coverage report --include=scripts/ci/run_summary.py --fail-under=80
```

The CI `coverage` job in `tests.yml` runs exactly this on every non-docs-only
change, then a combined informational report over the same two directories.
The `--source` flag means unimported files cannot hide from the report.

## Production-only denominator

Measured production code (repository CI tooling):

| Module | Stmts | Branch | Cover | Floor |
|---|---|---|---|---|
| `scripts/security/scorecard_guard.py` | 214 | 140 | 87% | >=80% (enforced) |
| `scripts/ci/run_summary.py` | 373 | 130 | 98% | >=80% (enforced) |

`run_summary.py` gained its unit suite in the #41 follow-up
(`tests/ci/test_run_summary.py`, 30 tests, stdlib-only, GitHub API mocked,
git calls faked): 98% measured, with the startup `_self_test` kept as the
first line of defense. Both production modules now carry the enforced 80%
branch floor. Uncovered lines (mostly `->exit` defensive paths and the
`__main__` guard) are visible in the CI report with `-m`.

## Excluded from the production denominator (justified)

- `prototype.py`, `intake_validation.py`: synthetic offline validation
  harnesses ("NOT production crypto or GitHub transport" per their own
  headers). Their unittest classes live inside the measured files, which is
  what inflated the historical 97.51% combined figure. Their self-runs stay
  in CI as functional checks; they are not production code, so coverage on
  them is not a quality signal.
- `test_requirements_pins.py`, `test_docs_vs_code.py`, `tests/`: test code.

No live submissions, credentials, paid runs or remote sweeps are involved;
all suites are synthetic/offline.
