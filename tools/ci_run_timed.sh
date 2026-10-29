#!/usr/bin/env bash
# Keep live output, per-phase timing and the command/pipeline's failure status.
# Python owns its child session and inner deadline; outer deadlines remain a backstop.
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
if [[ -e "$directory/python.started-at" ]]; then
  python3 tools/ci_run_process_group.py --verify-completion "$directory/python.lifecycle" || exit 125
fi
mkdir -p "$directory"
# Observe the JVM phase without moving its command into a new session or changing
# its deadline. The observer only reads /proc; it never signals measured PIDs.
if [[ "$phase" == jvm ]]; then
  # A new invocation invalidates old terminal evidence before probe startup.
  rm -f "$directory/jvm.time" "$directory/jvm.ended-at" "$directory/jvm.log" \
    "$directory/jvm.memory.json" "$directory/jvm.memory.json.partial" \
    "$directory/jvm.observer-cleanup.json" "$directory/jvm.observer-cleanup.json.partial"
  : > "$directory/jvm.time"
  : > "$directory/jvm.log"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/jvm.started-at"
  workload_status=unrun
  phase_finalized=false
  python3 tools/ci_observe_jvm_memory.py --root-pid "$$" --output "$directory/jvm.memory.json" &
  observer=$!
  observer_start=0
  observer_finalized=false
  observer_status=125
  observer_cleanup=false
  finish_observer() {
    if [[ "$observer_finalized" == true ]]; then return; fi
    observer_finalized=true
    if python3 tools/ci_observe_jvm_memory.py --stop-pid "$observer" --start-ticks "$observer_start" --output "$directory/jvm.observer-cleanup.json"; then
      observer_cleanup=true
      # pidfd polling established exit; this wait cannot wait on a live process.
      observer_status=0
      wait "$observer" || observer_status=$?
    fi
  }
  finish_on_exit() {
    local original=$?
    finish_observer
    if (( original == 0 && observer_status != 0 )); then original=125; fi
    # Bash can enter EXIT after a signal with a prior successful shell status.
    # An unrun/interrupted workload must never acquire a successful receipt.
    if (( original == 0 )) && [[ "$workload_status" == unrun || "$workload_status" == interrupted ]]; then original=125; fi
    if [[ "$phase_finalized" == false ]]; then
      printf 'workload_exit_status=%s\nobserver_exit_status=%s\nobserver_cleanup_complete=%s\nexit_status=%s\n' "$workload_status" "$observer_status" "$observer_cleanup" "$original" >> "$directory/jvm.time"
      date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/jvm.ended-at"
    fi
    exit "$original"
  }
  trap finish_on_exit EXIT
  if [[ -r "/proc/$observer/stat" ]]; then
    observer_stat=$(cat "/proc/$observer/stat")
    observer_stat=${observer_stat##*) }
    read -r -a observer_fields <<< "$observer_stat"
    observer_start=${observer_fields[19]:-0}
  fi
  # Wait for handlers and the first atomic sample before a fast command can end.
  # This bounded setup is inside the existing Actions step, not extra test time.
  for (( sample_wait=0; sample_wait<500; sample_wait++ )); do
    [[ -f "$directory/jvm.memory.json" ]] && break
    kill -0 "$observer" 2>/dev/null || exit 125
    sleep .01
  done
  [[ -f "$directory/jvm.memory.json" ]] || exit 125
fi
if [[ "$phase" != jvm ]]; then date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.started-at"; fi
TIMEFORMAT=$'real_seconds=%R\nuser_seconds=%U\nsys_seconds=%S'
status=0
if [[ "$phase" == jvm ]]; then workload_status=interrupted; fi
{ time "$@" 2>&1 | tee "$directory/$phase.log"; } 2> "$directory/$phase.time" || status=$?
if [[ "$phase" == jvm ]]; then
  workload_status=$status
  finish_observer
  if (( status == 0 && observer_status != 0 )); then status=125; fi
  printf 'workload_exit_status=%s\nobserver_exit_status=%s\nobserver_cleanup_complete=%s\n' "$workload_status" "$observer_status" "$observer_cleanup" >> "$directory/$phase.time"
fi
printf 'exit_status=%s\n' "$status" >> "$directory/$phase.time"
date -u +%Y-%m-%dT%H:%M:%SZ > "$directory/$phase.ended-at"
if [[ "$phase" == jvm ]]; then phase_finalized=true; fi
exit "$status"
