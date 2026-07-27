"""
compare_by_agent.py

Compares revert PR metrics across different AI agents
(Claude, Copilot, Cursor, Devin, OpenAI Codex).

Inputs:
- revert_metrics_full.csv  (output from get_pr_metrics.py)
- revert_prs_ready.csv     (contains the 'agent' column)

Outputs:
- agent_comparison.csv         (metrics broken down by agent)
- agent_comparison_summary.txt (easy to read summary for meetings)

Usage:
    python compare_by_agent.py
"""

import pandas as pd
import os

# ── Input files ───────────────────────────────────────────────────────────────
METRICS_FILE = "revert_metrics_full.csv"
AGENT_FILE   = "revert_prs_ready.csv"
OUT_CSV      = "agent_comparison.csv"
OUT_TXT      = "agent_comparison_summary.txt"

def main():
    # ── Load files ────────────────────────────────────────────────────────────
    if not os.path.exists(METRICS_FILE):
        print(f"[ERROR] {METRICS_FILE} not found. Run get_pr_metrics.py first.")
        return
    if not os.path.exists(AGENT_FILE):
        print(f"[ERROR] {AGENT_FILE} not found.")
        return

    metrics_df = pd.read_csv(METRICS_FILE)
    agent_df   = pd.read_csv(AGENT_FILE)[["id", "agent"]].drop_duplicates()

    # ── Merge agent info into metrics ─────────────────────────────────────────
    df = metrics_df.merge(agent_df, on="id", how="left")

    missing_agent = df["agent"].isna().sum()
    if missing_agent > 0:
        print(f"[WARN] {missing_agent} PRs could not be matched to an agent — they will be excluded.")

    df = df[df["agent"].notna()].copy()

    # Normalize agent names to lowercase for consistency
    df["agent"] = df["agent"].str.strip().str.lower()

    print(f"\nAgents found in dataset: {sorted(df['agent'].unique())}")
    print(f"Total PRs with agent info: {len(df)}\n")

    # ── Metrics to compare ────────────────────────────────────────────────────
    numeric_cols = [
        "time_to_close_hours",
        "time_to_close_days",
        "body_length",
        "commits",
        "changed_files",
        "additions",
        "deletions",
        "code_churn",
        "review_iterations",
        "total_comments",
        "reviewer_workload_hours",
    ]

    # ── Per-agent counts and acceptance rate ──────────────────────────────────
    agent_counts = df.groupby("agent").agg(
        total_prs=("id", "count"),
        merged=("is_merged", lambda x: (x.astype(str).str.lower() == "true").sum()),
        closed_or_merged=("state", lambda x: (x.str.lower() == "closed").sum()),
    ).reset_index()

    agent_counts["acceptance_rate"] = (agent_counts["merged"] / agent_counts["total_prs"]).round(4)

    # ── Per-agent averages for numeric metrics ────────────────────────────────
    agent_avgs = df.groupby("agent")[numeric_cols].mean().round(3).reset_index()
    agent_avgs.columns = ["agent"] + [f"avg_{c}" for c in numeric_cols]

    # ── Combine ───────────────────────────────────────────────────────────────
    result = agent_counts.merge(agent_avgs, on="agent")
    result.to_csv(OUT_CSV, index=False)
    print(f"[OK] Saved detailed comparison to: {OUT_CSV}")

    # ── Human readable summary ────────────────────────────────────────────────
    lines = []
    lines.append("=" * 60)
    lines.append("  REVERT PR METRICS BY AGENT — SUMMARY")
    lines.append("=" * 60)

    for _, row in result.iterrows():
        lines.append(f"\n── {row['agent'].upper()} ──────────────────────────────")
        lines.append(f"  Total revert PRs:        {int(row['total_prs'])}")
        lines.append(f"  Merged:                  {int(row['merged'])}")
        lines.append(f"  Acceptance rate:         {row['acceptance_rate']*100:.1f}%")
        lines.append(f"  Avg time to close:       {row['avg_time_to_close_hours']:.2f} hours")
        lines.append(f"  Avg commits:             {row['avg_commits']:.2f}")
        lines.append(f"  Avg changed files:       {row['avg_changed_files']:.2f}")
        lines.append(f"  Avg code churn (lines):  {row['avg_code_churn']:.0f}")
        lines.append(f"  Avg review iterations:   {row['avg_review_iterations']:.2f}")
        lines.append(f"  Avg total comments:      {row['avg_total_comments']:.2f}")

    lines.append("\n" + "=" * 60)
    lines.append("  QUICK COMPARISON TABLE")
    lines.append("=" * 60)

    # Print a simple ranked table for key metrics
    key_metrics = [
        ("acceptance_rate", "Acceptance Rate", lambda x: f"{x*100:.1f}%"),
        ("avg_time_to_close_hours", "Avg Time to Close (hrs)", lambda x: f"{x:.2f}"),
        ("avg_code_churn", "Avg Code Churn (lines)", lambda x: f"{x:.0f}"),
        ("avg_review_iterations", "Avg Review Iterations", lambda x: f"{x:.2f}"),
        ("avg_total_comments", "Avg Total Comments", lambda x: f"{x:.2f}"),
        ("total_prs", "Total PRs", lambda x: f"{int(x)}"),
    ]

    for col, label, fmt in key_metrics:
        lines.append(f"\n  {label}:")
        ranked = result[["agent", col]].sort_values(col, ascending=False)
        for _, r in ranked.iterrows():
            lines.append(f"    {r['agent'].upper():<20} {fmt(r[col])}")

    summary_text = "\n".join(lines)
    print(summary_text)

    with open(OUT_TXT, "w") as f:
        f.write(summary_text)
    print(f"\n[OK] Saved summary to: {OUT_TXT}")

if __name__ == "__main__":
    main()
