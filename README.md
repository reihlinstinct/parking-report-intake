# Encrypted report intake prototype

[![tests](https://github.com/reihlinstinct/parking-report-intake/actions/workflows/tests.yml/badge.svg)](https://github.com/reihlinstinct/parking-report-intake/actions/workflows/tests.yml)

Documentation and synthetic tests only. **Not accepting real reports.** Never publish reporter details, real vehicle plates, photos, credentials, keys or tokens here, in plaintext or encrypted, until the pilot has an approved go-live.

Every workflow ends with a `Run summary` job that writes a summary to the top of the run page: which jobs ran, their result and duration, what was skipped and why, the commits and files the run changed, and which checks cover those changes (`.github/ci-coverage-map.json` declares the coverage; files matching no mapping are flagged). The script is `scripts/ci/run_summary.py`.

This repository explores a public encrypted mailbox: one logical package contains an evidence JPEG and report JSON, encrypted on-device; only a separate private worker could decrypt. A public encryption key does not identify or authorize a sender. Device signatures, enrolled GitHub identities, exact approval, revocation, byte caps and durable duplicate guards are required.

Current status: eight offline crypto/package experiments and eight intake-boundary tests passed. Live GitHub App device-flow permissions, chunk acceptance, photo legibility, Android interoperability and private-worker triggering are unproven. No municipal calls or filing workflow in this repository. Public ciphertext and author/time/size metadata can be archived indefinitely. Do not use this as a production service.

Protocol: [PROTOCOL.md](PROTOCOL.md). Experimental test script: [prototype.py](prototype.py). Test dependencies are pinned in [requirements-test.txt](requirements-test.txt) (`pip install -r requirements-test.txt`). Run `python prototype.py` locally. Keys are generated transiently for synthetic tests and not written to disk.

No license selected. No permission to redistribute production code is implied.

Prototype API (synthetic, offline; see [prototype.py](prototype.py)):

- `encode(value)` - canonical JSON bytes (sorted keys, no spaces, UTF-8).
- `package(photo)` - build the bounded binary container (magic, header length, canonical JSON header, JPEG bytes) for a synthetic report.
- `unpack(value)` - parse and verify the container; rejects bad magic, header abuse and photo/approval digest mismatches.
- `encrypt(public, plaintext)` / `decrypt(private, blob)` - reviewed-library hybrid envelope (RSA-OAEP wrapped AES-GCM key) over the supplied plaintext. Neither function signs or verifies anything: the caller signs the plaintext package and verifies the signature separately.
- `chunks(blob)` / `assemble(parts)` - split the ciphertext into bounded base64 chunks and reassemble with count/index/digest validation.
- `synthetic_jpeg()` - deterministic synthetic evidence JPEG for the offline tests.
- `validate(...)` in [intake_validation.py](intake_validation.py) - the untrusted-transport boundary checks (manifest/chunk/enrollment shape).

Boundary test source: [intake_validation.py](intake_validation.py), run `python intake_validation.py`. Uses only Python standard library. This validates untrusted transport structure, not real identity enrollment, crypto authenticity or filing approval.

[test_requirements_pins.py](test_requirements_pins.py) (stdlib only) checks `requirements-test.txt`'s pins against what's actually installed; run `python test_requirements_pins.py`.
