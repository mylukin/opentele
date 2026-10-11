# Implementation notes

## 2026-10-11 — Adopt maintained OpenTele base

- User selected stufently/opentele as the maintained base while retaining mylukin/opentele. Merge preserves original history from `1a6f0816eac47ff3cb907af72ed9f8cbbbe8fba0` and maintained HEAD `6a17bc6cc49250fcad29f9fb400d7cf4dfb003c7` (opentele-ng 1.4.2). Changes are isolated in `codex/stable-refresh`.
- Baseline Python 3.14 import failed on `__firstlineno__` in upstream's class decorator. The maintained base fixes this and the Telethon positional API-hash bug; our synthetic client/profile/SQLite tests passed against published 1.4.2 before adoption.
- Current stable runtime versions: Telethon 1.45.0, tgcrypto-pyrofork 1.2.8; retained maintained hash-locked runtime requirements. Qt is test-only. Telethon v2 is a separate migration, not a dependency bump.
- Verify newest Desktop 7.3.1 against official version.h and api.tl at that tag: protocol layer 230. Add its verified mapping with a failing regression first. Telethon 1.45.0 uses layer 229, so default advertised version must remain a matching 7.2.9. A mapping update does not prove current Desktop tdata compatibility.
- Keep upstream package/import namespace (opentele-ng / opentele), with local version suffix `+mylukin.1` and source URL pointing to this fork. Do not install opentele and opentele-ng into the same environment.
- Upstream automatic tagging, PyPI/GHCR publication, docs deployment and issue-generating watch jobs stay gated to stufently/opentele; our fork does not publish or send maintenance messages implicitly.
- Legacy tests/tdata_test.py modifies source during collection and can terminate Telegram sessions. Default test configuration excludes it. All current verification uses synthetic sessions and keys; existing login experiment is untouched.
- Full Qt byte-equivalence, offline conversion and data-integrity tests are relevant because the maintained base replaces the tdata parser. A passing synthetic roundtrip does not prove a real Telegram Desktop or live Telegram login.
- Verified locally: Python 3.14.7 offline suite 384 passed / 3 skipped / 85.10% coverage; Python 3.12.9 wheel-install client suite 19 passed. Ruff, actionlint, sdist and wheel builds passed. Fork comparison and exact upstream links are in docs/fork-maintenance.md.
