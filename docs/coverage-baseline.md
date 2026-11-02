# Coverage baseline (#14)

Recorded 2026-11-02 against default-branch SHA
`34c84c46c1e7694849ea24601052d0cd80e19bb5` (pre-PR `main`).

## Test command

```sh
coverage run --branch --include=scripts/security/scorecard_guard.py \
  -m pytest tests/security/test_scorecard_guard.py -q
coverage report --fail-under=80
```

The CI `coverage` job in `tests.yml` runs exactly this on every non-docs-only
change, then a combined informational report adding `scripts/ci/run_summary.py`.

## Production-only denominator

Measured production code (repository CI tooling):

| Module | Stmts | Branch | Cover | Floor |
|---|---|---|---|---|
| `scripts/security/scorecard_guard.py` | 214 | 140 | 87% | >=80% (enforced) |
| `scripts/ci/run_summary.py` | 373 | 130 | 0% | N/A (see below) |

`run_summary.py` has no unit test suite (only its startup `_self_test`); it is listed in the denominator (not
excluded) and its measured 0% (373 statements, 130 branches, never imported
by any suite) is published in the combined CI report, which is run with
`--source=scripts/security,scripts/ci` so unimported files cannot hide. The 80% floor
does not apply to it yet - it is exercised live by every Run summary gate in
every workflow, and dedicated tests are future work outside this issue's
scope. Uncovered guard lines (mostly `->exit` defensive paths) are visible in
the CI report with `-m`.

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
