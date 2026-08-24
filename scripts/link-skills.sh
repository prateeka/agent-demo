#!/usr/bin/env bash
# Link only the orchestrator into .cursor/skills and .claude/skills for IDE discovery.
# Step skills live in platform/skills/ — child agents read them; users do not invoke them.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORCH="../../platform/skills/destination-launch/orchestrator"

link_orchestrator() {
  local skills_root="$1"
  mkdir -p "$skills_root"
  # Remove old step symlinks from prior link-skills versions
  for old in "$skills_root"/destination-launch-*; do
  [[ -e "$old" && "$(basename "$old")" != destination-launch-orchestrator ]] && rm -f "$old"
  done
  ln -sfn "$ORCH" "$skills_root/destination-launch-orchestrator"
  echo "Orchestrator linked in $skills_root:"
  ls -la "$skills_root/destination-launch-orchestrator"
}

link_orchestrator "$ROOT/.cursor/skills"
link_orchestrator "$ROOT/.claude/skills"

echo "Step skills (not linked): platform/skills/destination-launch/steps/"
