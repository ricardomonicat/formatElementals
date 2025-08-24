# Ricardo Monicat Monorepo

Packages:
- `packages/actionformats` — scaffold for action format utilities
- `packages/elementals` — elementals framework (English-first)

## Quickstart (Linux/macOS)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e packages/actionformats[dev]
pip install -e packages/elementals[dev]
nox -s tests-3.12 -s lint -s type
```
