#!/usr/bin/env bash
# INC-0014 run-window launcher (D07-S01, batch H031-H033 v1: the SUBMIT fits).
#
# Waits until the owner's window opens (21:00 Europe/Amsterdam = 19:00Z on 2026-10-03),
# then runs the allocated queue in order, one experiment at a time (scripts/run_experiment.py
# holds the INC-0008 lock). A run starts only if now + its pessimistic runtime <= window end
# (22:00); otherwise it is DEFERRED (left ALLOCATED, never started). A blend starts only if
# its components are COMPLETE and have passed their route checks (E042, the first routed
# SUBMIT instance, has no reference: it is marked checked on COMPLETE and cross-checked by
# E043's route check, whose reference it is). Running experiments are never
# killed here (the runner's class timeout bounds them). After each run: route check
# (prediction files only, no truth), then the brief §13 checkpoint commit and push of that
# run's own records only, so the next run records a clean tree. Log:
# runtime/run_window_D07-S01.log (git-ignored; copied into the session record afterwards).
set -u
export TZ=Europe/Amsterdam
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
LOG="runtime/run_window_D07-S01.log"
START=$(date -u -d "2026-10-03 19:00:00" +%s)
END=$(date -u -d "2026-10-03 20:00:00" +%s)

# id  pessimistic_s  components_that_must_be_COMPLETE_and_route_checked (comma list; - none)
# route reference for the run's own route check (- = none)
QUEUE=(
  "E042 700 - -"
  "E043 1100 - E042"
  "E044 60 E042,E043 -"
)

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }
status() { uv run python -c "import sys; sys.path.insert(0,'src'); from prc import ledger; r=ledger.get('$1'); print(r['status'] if r else 'MISSING')"; }
checkpoint() {  # $1 = experiment id; stages only that run's own records
  local eid=$1 paths=("experiments/$eid" "experiments/ledger.jsonl")
  [ -f "research/comparisons/route_check_$eid.json" ] && paths+=("research/comparisons/route_check_$eid.json")
  git add -- "${paths[@]}"
  git commit -q -m "$eid run records (INC-0014 window launcher checkpoint)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && log "$eid committed" || log "$eid nothing to commit"
  timeout 60 git push -q origin day-7 >>"$LOG" 2>&1 && log "pushed" || log "PUSH FAILED (commit kept locally)"
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
  read -r eid pess deps ref <<<"$item"
  blocked=""
  if [ "$deps" != "-" ]; then
    for dep in ${deps//,/ }; do
      if [ "$(status "$dep")" != "COMPLETE" ] || [ "${ROUTE_OK[$dep]:-no}" != "yes" ]; then
        blocked="$dep"; break
      fi
    done
  fi
  if [ -n "$blocked" ]; then
    log "$eid DEFERRED: component $blocked not COMPLETE or not route-checked"; continue
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
  [ "$(date +%s)" -gt "$END" ] && log "$eid ENDED AFTER WINDOW (INC-0014 deviation)"
  if [ "$st" = "COMPLETE" ]; then
    if [ "$ref" = "-" ]; then
      ROUTE_OK[$eid]=yes; log "$eid no route reference (cross-checked by a later run)"
    elif [ "$(status "$ref")" != "COMPLETE" ]; then
      log "$eid route_check NOT RUN: reference $ref not COMPLETE"
    elif uv run python scripts/route_check.py "$eid" - "$ref" >>"$LOG" 2>&1; then
      ROUTE_OK[$eid]=yes; ROUTE_OK[$ref]=yes; log "$eid route_check PASS against $ref"
    else
      ROUTE_OK[$ref]=no; log "$eid route_check FAIL against $ref (INVALID under its integrity clause)"
    fi
  fi
  checkpoint "$eid"
done
log "queue done; window ends $(date -d @"$END" +%H:%M) $TZ"
