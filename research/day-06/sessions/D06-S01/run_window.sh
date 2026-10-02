#!/usr/bin/env bash
# INC-0012 run-window launcher (D06-S01, batch X-D06-S01-0001).
#
# Waits until the owner's window opens (21:00 local, CEST = 19:00Z), then runs the
# allocated queue in order, one experiment at a time (scripts/run_experiment.py holds the
# INC-0008 lock). A run starts only if now + its pessimistic runtime <= window end (21:30);
# otherwise it is DEFERRED (left ALLOCATED, never started). A blend starts only if its
# component is COMPLETE and has passed its route check. Running experiments are never
# killed here. After each run: route check (prediction files only, no truth), then the
# brief §13 checkpoint commit and push of the run's records, so the next run records a
# clean tree. Log: runtime/run_window_D06-S01.log (git-ignored; copied into the session
# record after the window).
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
LOG="runtime/run_window_D06-S01.log"
START=$(date -d "2026-10-02 21:00:00" +%s)
END=$(date -d "2026-10-02 21:30:00" +%s)

# id  pessimistic_s  component_that_must_be_COMPLETE_and_route_checked (- for none)
QUEUE=(
  "E035 1000 -"
  "E036 60 E035"
  "E037 60 -"
  "E038 950 -"
  "E039 60 E038"
)

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {
  git add -A
  git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "committed: $1" || log "nothing to commit"
  git push -q origin day-6 >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
}

declare -A ROUTE_OK
log "launcher armed; window $(date -d @"$START" +%H:%M)-$(date -d @"$END" +%H:%M) local"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at arming"; exit 2; }
while [ "$(date +%s)" -lt "$START" ]; do sleep 10; done
log "window open"

for item in "${QUEUE[@]}"; do
  read -r eid pess dep <<<"$item"
  if [ "$dep" != "-" ]; then
    if [ "$(status "$dep")" != "COMPLETE" ] || [ "${ROUTE_OK[$dep]:-no}" != "yes" ]; then
      log "$eid DEFERRED: component $dep not COMPLETE or not route-checked"; continue
    fi
  fi
  now=$(date +%s)
  if [ $((now + pess)) -gt "$END" ]; then
    log "$eid DEFERRED: needs ${pess}s, $((END - now))s left in window"; continue
  fi
  log "$eid START (pessimistic ${pess}s)"
  uv run python scripts/run_experiment.py "$eid" >>"$LOG" 2>&1
  rc=$?
  log "$eid END rc=$rc status=$(status "$eid")"
  if [ "$(status "$eid")" = "COMPLETE" ]; then
    if uv run python scripts/route_check.py "$eid" - E029 >>"$LOG" 2>&1; then
      ROUTE_OK[$eid]=yes; log "$eid route_check PASS"
    else
      log "$eid route_check FAIL (INVALID under its integrity clause)"
    fi
  fi
  checkpoint "$eid run records (INC-0012 window launcher checkpoint)"
done
log "queue done; window ends $(date -d @"$END" +%H:%M) local"
