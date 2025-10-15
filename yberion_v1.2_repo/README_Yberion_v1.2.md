# Yberion v1.2 - Room Zero Package

Export date: 2025-10-08T22:56:03.088577

This repository is an export of the Yberion v1.2 Room Zero sandbox system.
It is designed to be integrated locally into your Room Zero host.

## Structure
- `src/` - core modules, agents, mirror, utils
- `tests/` - pytest suite for new modules
- `scripts/` - helper scripts (create git history locally, run roomzero locally)
- `README_Yberion_v1.2.md` - human readable release notes
- `CHANGELOG.md` - release history

## How to use
1. Unzip the package
2. (Optional) create a virtualenv and install test deps `pip install pytest`
3. Run tests: `pytest -q tests/`
4. To create a local git history and tags (simulated), run `bash scripts/create_git_history.sh` in the repo root.
5. Run the Room Zero sample runner: `bash scripts/run_roomzero.sh`

## Safety & Autonomy
This package does NOT create persistent autonomous processes by itself.
The `scripts/run_roomzero.sh` is a local runner that triggers simulated Task flows; it will not autonomously run in the background.
The `scripts/create_git_history.sh` will create a real `.git` history locally when executed by you.
