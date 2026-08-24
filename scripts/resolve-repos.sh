#!/usr/bin/env bash
# Resolve code repo paths. Run from agent-demo root.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${LAUNCHPAD_DIST:-}" || -z "${LAUNCHPAD_DIST_TYPES:-}" ]]; then
  echo "ERROR: Set LAUNCHPAD_DIST and LAUNCHPAD_DIST_TYPES before running code steps." >&2
  echo "  export LAUNCHPAD_DIST=/path/to/dist" >&2
  echo "  export LAUNCHPAD_DIST_TYPES=/path/to/dist_types" >&2
  exit 1
fi

DIST="$LAUNCHPAD_DIST"
DIST_TYPES="$LAUNCHPAD_DIST_TYPES"
if [[ "$DIST" != /* ]]; then DIST="$ROOT/$DIST"; fi
if [[ "$DIST_TYPES" != /* ]]; then DIST_TYPES="$ROOT/$DIST_TYPES"; fi

echo "agent-demo=$ROOT"
echo "dist=$DIST"
echo "dist_types=$DIST_TYPES"
