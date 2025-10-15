#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"
if [ -d .git ]; then
  echo ".git already exists. Exiting."
  exit 0
fi
git init
git config user.name "Yberion"
git config user.email "yberion@example.com"
git add .
git commit -m "chore: initial import of yberion v1.2"
git tag -a v1.2 -m "Yberion v1.2"
# create a few simulated commits to build history
echo "checkpoint" >> src/mirror/memory_summarizer.py
git add src/mirror/memory_summarizer.py
git commit -m "feat: memory summarizer checkpoint tweak"
echo "adaptive" >> src/mirror/adaptive_balancer.py
git add src/mirror/adaptive_balancer.py
git commit -m "feat: adaptive balancer tuning"
git tag -a v1.2-alpha -m "alpha"
echo "done" > DEPLOYED.txt
git add DEPLOYED.txt
git commit -m "chore: deployment marker"
echo "Local git history generated."
