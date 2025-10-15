#!/usr/bin/env bash
set -euo pipefail

# --------- Configuration (edit these if needed) ----------
ZIP_FILE="yberion_v2.1_protocol.zip"   # ensure this is in current dir
TARGET_DIR="yberion_v2.1_protocol"
REPO_DIR="${PWD}/yberion_repo"         # where the repo will be created
GIT_USER_NAME="Yberion"
GIT_USER_EMAIL="yberion@kal.el"
INITIAL_TAG="v2.1"
BRANCH="feat/protocol-stack"
# If you want to push, set REMOTE_URL; otherwise leave empty.
REMOTE_URL="git@github.com:yberion-bot/yberion.git" # "https://github.com/yberion-bot/yberion.git" # e.g. "git@github.com:yourname/yberion.git" or "https://github.com/yourname/yberion.git"
# ---------------------------------------------------------

echo "1) Preparing workspace..."
if [ -d "$TARGET_DIR" ]; then
  rm -rf "$TARGET_DIR"
fi
if [ -d "$REPO_DIR" ]; then
  rm -rf "$REPO_DIR"
fi
mkdir -p "$TARGET_DIR"

if [ ! -f "$ZIP_FILE" ]; then
  echo "ERROR: ZIP $ZIP_FILE not found in $(pwd)"
  echo "Place the downloaded yberion_v2.1_protocol.zip into this folder or update ZIP_FILE in the script."
  exit 2
fi

echo "2) Unzipping $ZIP_FILE ..."
unzip -q "$ZIP_FILE" -d "$TARGET_DIR"

echo "3) Creating git repo at $REPO_DIR ..."
mkdir -p "$REPO_DIR"
cp -r "$TARGET_DIR"/* "$REPO_DIR"/

cd "$REPO_DIR"

if [ -d .git ]; then
  echo "Existing .git found, aborting to avoid overwriting existing repo. Remove .git if you want to reinitialize."
  exit 3
fi

echo "4) Initializing git and making initial commits ..."
git init
# git config user.name "$GIT_USER_NAME"
# git config user.email "$GIT_USER_EMAIL"

# First import commit
git add .
git commit -m "chore: import Yberion v2.1 protocol scaffolding"

# Create a few incremental commits to simulate history (optional)
echo "# checkpoint" >> src/agents/prompt_optimizer.py
git add src/agents/prompt_optimizer.py
git commit -m "feat: prompt optimizer baseline tweak"

echo "# registry update" >> src/registry/agent_registry.py
git add src/registry/agent_registry.py
git commit -m "feat: agent registry baseline"

git branch -M main
git checkout -b "$BRANCH"

# Tagging
git tag -a "$INITIAL_TAG" -m "Yberion v2.1 - Protocol & Governance"

# Optional: set remote and push (only if you configured REMOTE_URL)
if [ -n "$REMOTE_URL" ]; then
  git remote add origin "$REMOTE_URL"
  echo "Pushing branches and tags to remote..."
  git push -u origin main
  git push -u origin "$BRANCH"
  git push origin "$INITIAL_TAG"
else
  echo "No remote push configured (REMOTE_URL empty). If you want to push, set REMOTE_URL in the script."
fi

echo "5) (Optional) Create python venv, install pytest and run tests"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  PY="C:\Users\schat\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe"
fi

if [ -n "$PY" ]; then
  if [ ! -d .venv ]; then
    $PY -m venv .venv
  fi
  # activate venv for this script
  # shellcheck disable=SC1091
  source .venv/bin/activate || source .venv/Scripts/activate || true
  pip install --upgrade pip >/dev/null
  pip install pytest >/dev/null
  # run tests if tests exist
  if [ -d tests ]; then
    echo "Running pytest..."
    pytest -q || echo "Some tests failed — check output above."
  else
    echo "No tests/ folder found — skip pytest."
  fi
  deactivate || true
else
  echo "Python not found in PATH — skipping pytest steps."
fi

echo "6) Done. Repository available at: $REPO_DIR"
echo " - to inspect: cd $REPO_DIR"
echo " - to see commits: git log --oneline --graph --decorate"
echo " - to run tests manually: source .venv/bin/activate; pytest -q"
