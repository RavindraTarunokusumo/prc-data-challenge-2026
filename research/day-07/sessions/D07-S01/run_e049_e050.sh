#!/usr/bin/env bash
# INC-0016 run script (D07-S01; P5 (b) of X-D07-S01-0003): the deferred SUBMIT runs E049
# (H036 v1) then E050 (H037 v1), started by the researcher only on the owner's go.
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
LOG="runtime/run_D07-S01_e049_e050.log"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {  # $1 = experiment id; stages only that run's own records
  local eid=$1 paths=("experiments/$eid" "experiments/ledger.jsonl")
  [ -f "research/comparisons/route_check_$eid.json" ] && paths+=("research/comparisons/route_check_$eid.json")
  git add -- "${paths[@]}"
  git commit -q -m "$eid run records (INC-0016 run-script checkpoint)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "$eid committed" || log "$eid nothing to commit"
  timeout 60 git push -q origin day-7 >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
  local extra; extra=$(git status --porcelain)
  [ -n "$extra" ] && log "WARNING: tree not clean after $eid checkpoint: $(echo "$extra" | tr '\n' ' ')"
}

log "start (owner's go)"
[ -n "$(git status --porcelain)" ] && { log "ABORT: tree not clean at start"; exit 2; }
[ "$(status E049)" = "ALLOCATED" ] || { log "ABORT: E049 is not ALLOCATED"; exit 2; }

log "E049 START"
uv run python scripts/run_experiment.py E049 >>"$LOG" 2>&1
log "E049 END rc=$? status=$(status E049)"
checkpoint E049
if [ "$(status E049)" != "COMPLETE" ]; then
  log "E050 NOT STARTED: E049 not COMPLETE"; log "done"; exit 1
fi

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
