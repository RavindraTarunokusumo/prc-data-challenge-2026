#!/usr/bin/env bash
# INC-0016 run script, part 2 (D07-S01; P5 (b) of X-D07-S01-0003; U10 deferral): E050
# (H037 v1) only. run_e049_e050.sh ran E049 (COMPLETE) and then stopped in its checkpoint
# function on an unbound variable (`local eid=$1 paths=(... $eid ...)` expands $eid before
# assigning it; the launchers had a global $eid). This copy fixes only that line and drops
# the E049 steps.
#
# Direct scripts/run_experiment.py calls (the INC-0008 lock), each followed by the pinned
# launchers' own-path checkpoint (commit and push of that run's records only), so E050 runs
# on a committed E049. E050 starts only if E049 is COMPLETE. After E050: route check
# E050 E044 E049 (prediction files only, no truth), then E050's checkpoint. Never kills a
# run (the class timeout bounds it). Log: runtime/run_D07-S01_e049_e050.log (git-ignored;
# copied into the session record afterwards).
set -u
export TZ=Europe/Amsterdam
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
LOG="runtime/run_D07-S01_e050.log"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {  # $1 = experiment id; stages only that run's own records
  local eid=$1
  local paths=("experiments/$eid" "experiments/ledger.jsonl")
  [ -f "research/comparisons/route_check_$eid.json" ] && paths+=("research/comparisons/route_check_$eid.json")
  git add -- "${paths[@]}"
  git commit -q -m "$eid run records (INC-0016 run-script checkpoint)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "$eid committed" || log "$eid nothing to commit"
  timeout 60 git push -q origin day-7 >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
  local extra; extra=$(git status --porcelain)
  [ -n "$extra" ] && log "WARNING: tree not clean after $eid checkpoint: $(echo "$extra" | tr '\n' ' ')"
}

log "start (owner's go, INC-0016; part 2)"
extra=$(git status --porcelain)
[ "$extra" = " M orchestration/task-ledger.jsonl" ] || { log "ABORT: tree state is not the pre-registered one (task ledger only): $extra"; exit 2; }
[ "$(status E049)" = "COMPLETE" ] || { log "ABORT: E049 is not COMPLETE"; exit 2; }
[ "$(status E050)" = "ALLOCATED" ] || { log "ABORT: E050 is not ALLOCATED"; exit 2; }

log "E050 START"
uv run python scripts/run_experiment.py E050 >>"$LOG" 2>&1
st=$(status E050)
log "E050 END status=$st"
if [ "$st" = "COMPLETE" ]; then
  if uv run python scripts/route_check.py E050 E044 E049 >>"$LOG" 2>&1; then
    log "E050 route_check PASS against E044 and E049"
  else
    log "E050 route_check FAIL against E044 and E049 (INVALID under its integrity clause)"
  fi
fi
checkpoint E050
log "done"
