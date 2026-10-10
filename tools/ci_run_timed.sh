#!/usr/bin/env bash
# Keep live output, per-phase timing and the command/pipeline's failure status.
# Workflow step and job deadlines remain the cancellation authority.
set -euo pipefail
phase=${1:?Expected a phase name followed by a command}
shift
case "$phase" in python|jvm|lint) ;; *) echo "Unknown CI phase: $phase" >&2; exit 2 ;; esac
if (( $# == 0 )); then echo 'Expected a command' >&2; exit 2; fi
directory=build/reports/ci-phases
mkdir -p "$directory"
date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.started-at"
TIMEFORMAT=$'real_seconds=%R\nuser_seconds=%U\nsys_seconds=%S'
status=0
{ time "$@" 2>&1 | tee "$directory/$phase.log"; } 2> "$directory/$phase.time" || status=$?
printf 'exit_status=%s\n' "$status" >> "$directory/$phase.time"
date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.ended-at"
exit "$status"
