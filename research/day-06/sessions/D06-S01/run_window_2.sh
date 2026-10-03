#!/usr/bin/env bash
# INC-0012 run-window launcher (D06-S01, batch H029-H030 v1).
#
# Waits until the owner's window opens (21:00 Europe/Amsterdam = 19:00Z on 2026-10-03),
# then runs the allocated queue in order, one experiment at a time (scripts/run_experiment.py
# holds the INC-0008 lock). A run starts only if now + its pessimistic runtime <= window end
# (21:30); otherwise it is DEFERRED (left ALLOCATED, never started). A blend starts only if
# its component is COMPLETE and has passed its route check. Running experiments are never
# killed here (the runner's class timeout bounds them). After each run: route check
# (prediction files only, no truth), then the brief §13 checkpoint commit and push of that
# run's own records only, so the next run records a clean tree. Log:
# runtime/run_window_D06-S01_2.log (git-ignored; copied into the session record afterwards).
set -u
export TZ=Europe/Amsterdam
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
LOG="runtime/run_window_D06-S01_2.log"
START=$(date -u -d "2026-10-03 19:00:00" +%s)
END=$(date -u -d "2026-10-03 19:30:00" +%s)

# id  pessimistic_s  component_that_must_be_COMPLETE_and_route_checked (- for none)
QUEUE=(
  "E040 1600 -"
  "E041 60 E040"
)

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {  # $1 = experiment id; stages only that run's own records
  local eid=$1 paths=("experiments/$eid" "experiments/ledger.jsonl")
  [ -f "research/comparisons/route_check_$eid.json" ] && paths+=("research/comparisons/route_check_$eid.json")
  git add -- "${paths[@]}"
  git commit -q -m "$eid run records (INC-0012 window launcher checkpoint)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "$eid committed" || log "$eid nothing to commit"
  timeout 60 git push -q origin day-6 >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
  local extra; extra=$(git status --porcelain)
  [ -n "$extra" ] && log "WARNING: tree not clean after $eid checkpoint: $(echo "$extra" | tr '\n' ' ')"
}

declare -A ROUTE_OK
log "launcher armed; window $(date -d @"$START" +%H:%M)-$(date -d @"$END" +%H:%M) $TZ"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at arming"; exit 2; }
while [ "$(date +%s)" -lt "$START" ]; do sleep 10; done
log "window open"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at window open"; exit 2; }

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
  st=$(status "$eid")
  log "$eid END rc=$rc status=$st"
  [ "$(date +%s)" -gt "$END" ] && log "$eid ENDED AFTER WINDOW (INC-0012 deviation)"
  if [ "$st" = "COMPLETE" ]; then
    if uv run python scripts/route_check.py "$eid" - E029 >>"$LOG" 2>&1; then
      ROUTE_OK[$eid]=yes; log "$eid route_check PASS"
    else
      log "$eid route_check FAIL (INVALID under its integrity clause)"
    fi
  fi
  checkpoint "$eid"
done
log "queue done; window ends $(date -d @"$END" +%H:%M) $TZ"
