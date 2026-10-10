# mylukin fork maintenance — 2026-10-11

## Source and choice

The user selected the maintained stufently base while keeping `mylukin/opentele`.
The merge preserves history from original OpenTele
`1a6f0816eac47ff3cb907af72ed9f8cbbbe8fba0` to maintained HEAD
`6a17bc6cc49250fcad29f9fb400d7cf4dfb003c7`.

This was a bounded public-fork comparison, not a claim of global popularity or activity.

| Candidate | Substantive source evidence | Assessment |
| --- | --- | --- |
| [stufently/opentele](https://github.com/stufently/opentele) / opentele-ng 1.4.2 | [2026-10-04 CLI session write/flush repair](https://github.com/stufently/opentele/commit/df0868ed323695668e9bc1daf290f32212e0599a), Python 3.10–3.14 CI, offline binary-format tests | Selected. Keeps `opentele` imports, removes Qt runtime and bounds Telethon below v2. |
| [DedInc/opentele2](https://github.com/DedInc/opentele2) / 1.2.1 | [2026-06-01 source changes](https://github.com/DedInc/opentele2/commit/e55fc3fc885bd3fb526feae4d93df37f2fa0adc6) | Alternative; different import namespace, no Telethon upper bound, no repository Actions run evidence found during comparison. |
| [Pavel-qr/opentele](https://github.com/Pavel-qr/opentele) | [2026-06-22 Python class metadata fix](https://github.com/Pavel-qr/opentele/commit/e9ad22c8502de897e93fef589e0ca5ba687a2ce0) | Useful narrow patch, less evidence of broad maintenance. |

## What OpenTele adds to Telethon

- Reads and writes Telegram Desktop tdata, including Qt-style binary fields,
  local encryption, DC configuration and stored authorization keys.
- Reuses an existing authorization (`UseCurrentSession`) or creates another
  authorization through the QR login flow (`CreateNewSession`). These are different operations.
- Supplies client API/device/language profiles and modifies Telethon's
  connection initialization. The inherited global class patching still exists.
- Adds helpers to inspect/terminate device authorizations and convert sessions.
  MTProto networking, normal phone login, reconnects and updates come from Telethon.

The original MIT license allows modification and redistribution while retaining
its notice. Preserve both original and maintained-fork attribution. Dependency
licenses remain separate. The selected fork has no Qt runtime dependency; Qt6
is installed only for binary-equivalence tests.

## Versions and boundaries

- Local fork version: `1.4.2+mylukin.1`, distribution `opentele-ng`, import `opentele`.
- Hash-locked runtime: Telethon 1.45.0, tgcrypto-pyrofork 1.2.8 and transitive dependencies.
- Tests used pytest 9.1.1, pytest-asyncio 1.4.0, Hypothesis 6.168.5,
  Ruff 0.17.0, PyQt6 6.11.0 and pyrofork 2.3.69.
- [Desktop v7.3.1 version.h](https://github.com/telegramdesktop/tdesktop/blob/v7.3.1/Telegram/SourceFiles/core/version.h)
  identifies the latest stable release checked during this task.
  Its [api.tl](https://github.com/telegramdesktop/tdesktop/blob/v7.3.1/Telegram/SourceFiles/mtproto/scheme/api.tl)
  declares layer 230. The new version table includes this verified mapping.
- Telethon 1.45.0 declares layer 229, so the default remains `7.2.9 x64`.
  Neither this mapping nor the `official_app` flag proves full official-client behavior.
- No Telethon v2 migration, real Desktop 7.3.1 tdata acceptance, live login or
  message reception was performed with this fork. The existing local login
  experiment was not changed.

## Verification

1. Original OpenTele failed import on Python 3.14 at `__firstlineno__`.
2. Before changing the maintained base, the new layer-230 regression failed;
   after adding the verified mapping it passed.
3. Python 3.14.7, full offline suite: **384 passed, 3 skipped**, 85.10% coverage
   against the inherited 78% gate. The dangerous legacy live test is excluded.
4. Python 3.12.9, fresh wheel install and focused client/session suite:
   **19 passed**. Package assets present; no PyQt module loaded at runtime.
5. Ruff, actionlint, source-distribution build and wheel build passed.

Commands (from repository root):

```sh
CI=true .venv-current/bin/python -m pytest --ignore=tests/tdata_test.py --cov=opentele --cov-report=term --cov-fail-under=78 tests/
CI=true .venv-current/bin/ruff check src/ tests/
actionlint
CI=true .venv-current/bin/python -m build
```

## Updating later

Keep `origin` pointed at mylukin/opentele and `maintained` at
https://github.com/stufently/opentele.git. Merge maintained commits into a branch,
review the delta, then repeat offline/session and wheel checks. A package
version update is not authorization to replace an active Telegram session.

Automatic tagging, PyPI/GHCR release, Pages deployment and issue-generating
watch workflows are gated to the upstream maintainer's repository. Do not
remove that gate until a separate distribution/publication decision is made.
Tests, lint and CodeQL remain available in this fork. Do not install both
`opentele` and `opentele-ng` into the same virtual environment.
