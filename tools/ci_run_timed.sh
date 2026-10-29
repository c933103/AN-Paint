#!/usr/bin/env bash
# Keep live output, per-phase timing and the command/pipeline's failure status.
# Python/JVM own their child sessions and inner deadlines; outer deadlines remain a backstop.
set -euo pipefail
phase=${1:?Expected a phase name followed by a command}
shift
case "$phase" in python|jvm|native|lint|apk) ;; *) echo "Unknown CI phase: $phase" >&2; exit 2 ;; esac
if (( $# == 0 )); then echo 'Expected a command' >&2; exit 2; fi
# exec makes this PID the signal-aware owner instead of an orphanable tee pipeline.
if [[ "$phase" == python ]]; then
  exec python3 tools/ci_run_process_group.py --timeout-seconds 1800 --kill-after-seconds 15 -- "$@"
fi
directory=build/reports/ci-phases
# A failed/absent cleanup receipt must never permit overlapping later phases.
for previous in python jvm; do
  if [[ "$phase" != "$previous" && -e "$directory/$previous.started-at" ]]; then
    python3 tools/ci_run_process_group.py --verify-completion "$directory/$previous.lifecycle" || exit 125
  fi
done
if [[ "$phase" == jvm ]]; then
  # Reserve one minute of the 25-minute step for cleanup/reporting.
  exec python3 tools/ci_run_process_group.py --phase jvm --timeout-seconds 1440 --kill-after-seconds 15 -- "$@"
fi
mkdir -p "$directory"
date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.started-at"
TIMEFORMAT=$'real_seconds=%R\nuser_seconds=%U\nsys_seconds=%S'
status=0
{ time "$@" 2>&1 | tee "$directory/$phase.log"; } 2> "$directory/$phase.time" || status=$?
printf 'exit_status=%s\n' "$status" >> "$directory/$phase.time"
date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.ended-at"
exit "$status"
