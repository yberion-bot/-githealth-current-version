#!/usr/bin/env bash
set -euo pipefail
echo "This script is a local simulation runner for Room Zero. It does not create persistent services."
echo "You can run python snippets from src/ to manually invoke NexusOrchestrator if desired."
echo "For example, run: python -c "from src.yberion_nexus import NexusOrchestrator; print('NexusReady')""
