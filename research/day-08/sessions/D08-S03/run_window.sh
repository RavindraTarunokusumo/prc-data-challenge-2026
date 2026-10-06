#!/usr/bin/env bash
# D08-S03 run-window launcher (batch H038 v1: the convention mixture).
#
#   bash research/day-08/sessions/D08-S03/run_window.sh "<START UTC>" "<END UTC>"
#
# START and END are the owner's window (UTC, `date -d` syntax), recorded in the log. Waits
# for START, then runs the allocated queue in order, one experiment at a time
# (scripts/run_experiment.py holds the INC-0008 lock). A run starts only if
# now + its pessimistic runtime <= END; otherwise it is DEFERRED (left ALLOCATED, never
# started). A run never starts after an earlier queue entry failed its integrity check.
# Running experiments are never killed here (the runner's class timeout bounds them).
# After each run: mixture_check.py EID E046 (prediction and component files only, no truth),
# then the brief §13 checkpoint commit and push of that run's own records only.
# Log: runtime/run_window_D08-S03.log (git-ignored; copied into the session record afterwards).
set -u
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
LOG="runtime/run_window_D08-S03.log"
[ $# -eq 2 ] || { echo "usage: $0 START_UTC END_UTC"; exit 2; }
START=$(date -u -d "$1" +%s) || exit 2
END=$(date -u -d "$2" +%s) || exit 2
BRANCH=day-8
BASE=E046

# id  pessimistic_s
QUEUE=(
  "E051 1500"
  "E052 1500"
)

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {  # $1 = experiment id; stages only that run's own records
  local eid=$1 paths=("experiments/$eid" "experiments/ledger.jsonl")
  [ -f "research/comparisons/mixture_check_$eid.json" ] && paths+=("research/comparisons/mixture_check_$eid.json")
  git add -- "${paths[@]}"
  git commit -q -m "$eid run records (D08-S03 window launcher checkpoint)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "$eid committed" || log "$eid nothing to commit"
  timeout 60 git push -q origin "$BRANCH" >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
  local extra; extra=$(git status --porcelain)
  [ -n "$extra" ] && log "WARNING: tree not clean after $eid checkpoint: $(echo "$extra" | tr '\n' ' ')"
}

log "launcher armed; window $(date -u -d @"$START" +%FT%TZ) to $(date -u -d @"$END" +%FT%TZ)"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at arming"; exit 2; }
while [ "$(date +%s)" -lt "$START" ]; do sleep 10; done
log "window open"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at window open"; exit 2; }

failed=""
for item in "${QUEUE[@]}"; do
  read -r eid pess <<<"$item"
  if [ -n "$failed" ]; then
    log "$eid DEFERRED: $failed failed its run or integrity check"; continue
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
  [ "$(date +%s)" -gt "$END" ] && log "$eid ENDED AFTER WINDOW (deviation)"
  if [ "$st" = "COMPLETE" ]; then
    if uv run python scripts/mixture_check.py "$eid" "$BASE" >>"$LOG" 2>&1; then
      log "$eid mixture_check PASS against $BASE"
    else
      log "$eid mixture_check FAIL against $BASE (INVALID under its integrity clause)"; failed=$eid
    fi
  else
    failed=$eid
  fi
  checkpoint "$eid"
done
log "queue done; window ends $(date -u -d @"$END" +%FT%TZ)"
