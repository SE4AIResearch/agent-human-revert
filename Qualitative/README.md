## Replication Scripts

### Fisher's Exact Tests
Two Fisher's exact tests are included as replication scripts:

- `fisher_exact_test.py` — Tests whether Documentation/Content Bloat is 
  proportionally more common in human Scope Creep reverts than AI Scope 
  Creep reverts (Section 5.2).

- `fisher_reviewer_activity.py` — Tests whether reviewer activity differs 
  significantly between AI agent and human revert PRs (Section 6.2).

**Requirements:** `pip install scipy statsmodels numpy`

**Usage:** `python fisher_exact_test.py` / `python fisher_reviewer_activity.py`
