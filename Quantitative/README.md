Quantitative README

## Replication Scripts
Four scripts are included as replication scripts:

* `get_pr_metrics.py` — Pulls PR-level metrics from the GitHub API (commits, additions, deletions, code churn, review iterations, comments, reviewer workload). Requires a `GITHUB_TOKEN` environment variable.
* `compare_pr_metrics.py` — Runs Shapiro-Wilk normality checks, Mann-Whitney U, and Cliff's Delta across all metrics for agent vs. human revert PRs.
* `spearman_correlation.py` — Generates Spearman rank correlation heatmaps for each group.
* `compare_by_agent.py` — Breaks down metrics by individual AI agent: OpenAI Codex, Devin, Copilot, Cursor, Claude Code.

Requirements: `pip install pandas numpy scipy matplotlib`
Usage: `python get_pr_metrics.py --ids <ids> --csv <input.csv> --out_full <out.csv> --out_summary <out.csv>` / `python compare_pr_metrics.py --file-a <agent.csv> --file-b <human.csv>` / `python spearman_correlation.py` / `python compare_by_agent.py`

## Data

- `agent_revert_prs.csv` / `human_revert_prs.csv` — final per-PR metrics for the datasets.
- `agent_comparison.csv` / `agent_comparison_summary.txt` — per-agent breakdown (output of `compare_by_agent.py`).
- `metrics_comparison_table.csv`, `metrics_summary_by_file.csv`, `metrics_long_concat.csv` — outputs of `compare_pr_metrics.py`.
- `plots` — box plots (one per metric) and Spearman correlation heatmaps (`corr_agent.png`, `corr_human.png`).

## Data Notes

- **Acceptance rate** is defined as the presence of a non-null `merged_at` timestamp, not merely a closed PR state (a rejected PR is also "closed" without being merged). This definition is used consistently across all scripts and outputs in this folder.
