---
schema: advisor-review-v1
hypothesis_id: H###
proposal_version: 1
proposal_sha256: HEX_DIGEST
exchange_id: X-D01-S01-0001
advisor: advisor-subagent
advisor_model: RESOLVED_MODEL_ID
advisor_policy: advisor-policy-v3.0
decision: ACCEPT | REVISE | REJECT | HOLD
confidence: 0.00
created_utc: YYYY-MM-DDTHH:MM:SSZ
---

# Advisor Review

## Summary Assessment
## Scientific Validity
## Novelty Relative to Existing Research
## Experimental Isolation
## Validation Quality
## Leakage Review
### Target Leakage
PASS | CONCERN | FAIL
### Temporal Leakage
PASS | CONCERN | FAIL
### Competition Availability
PASS | CONCERN | FAIL
## Compute Review
### RAM
PASS | REVISE | FAIL
### Runtime
PASS | REVISE | FAIL
### Disk
PASS | REVISE | FAIL
## Weakest Assumption
## Missing Control or Ablation
## Decision
ACCEPT | REVISE | REJECT | HOLD
## Execution Authorization
Authorized scope:
Required acknowledgement path:
## Revision
## Advisor Prediction
Probability of improvement:
Expected magnitude:
Primary expected failure mode:
