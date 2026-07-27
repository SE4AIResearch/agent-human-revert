"""
spearman_correlation.py

Generates Spearman rank correlation heatmaps for agent and human revert PR datasets.
Run from the New Quant folder:
    python spearman_correlation.py

Inputs:
    revert_metrics_full.csv   — agent PR metrics
    human_metrics_full.csv    — human PR metrics

Outputs:
    corr_agent.png            — correlation matrix heatmap for agent PRs
    corr_human.png            — correlation matrix heatmap for human PRs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# ── Settings ──────────────────────────────────────────────────────────────────
AGENT_FILE  = "revert_metrics_full.csv"
HUMAN_FILE  = "human_metrics_full.csv"
OUT_AGENT   = "corr_agent.png"
OUT_HUMAN   = "corr_human.png"

METRICS = [
    'time_to_close_hours',
    'body_length',
    'commits',
    'changed_files',
    'additions',
    'deletions',
    'code_churn',
    'review_iterations',
    'total_comments',
    'reviewer_workload_hours',
]

LABELS = [
    'Merge_Hours',
    'Desc_Length',
    'Commits',
    'Files',
    'Additions',
    'Deletions',
    'Churn',
    'Iterations',
    'Comments',
    'Workload',
]

# ── Functions ─────────────────────────────────────────────────────────────────
def compute_corr_matrix(df, cols):
    n = len(cols)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a = df[cols[i]].dropna()
            b = df[cols[j]].dropna()
            idx = a.index.intersection(b.index)
            if len(idx) > 2:
                r, _ = spearmanr(a.loc[idx], b.loc[idx])
                mat[i, j] = r
            else:
                mat[i, j] = np.nan
    return mat

def plot_heatmap(mat, labels, title, filename):
    fig, ax = plt.subplots(figsize=(9, 7))
    cmap = plt.cm.RdYlBu_r
    im = ax.imshow(mat, cmap=cmap, vmin=-1, vmax=1, aspect='auto')

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)

    for i in range(len(labels)):
        for j in range(len(labels)):
            val = mat[i, j]
            if not np.isnan(val):
                color = 'white' if abs(val) > 0.6 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=7.5, color=color, fontweight='bold')

    plt.colorbar(im, ax=ax, label='Spearman ρ', fraction=0.046, pad=0.04)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {filename}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    agent = pd.read_csv(AGENT_FILE)
    human = pd.read_csv(HUMAN_FILE)

    # Only keep columns that exist in each dataset
    agent_cols = [m for m in METRICS if m in agent.columns]
    human_cols = [m for m in METRICS if m in human.columns]
    agent_labels = [LABELS[METRICS.index(m)] for m in agent_cols]
    human_labels = [LABELS[METRICS.index(m)] for m in human_cols]

    print(f"[INFO] Agent PRs: {len(agent)}")
    print(f"[INFO] Human PRs: {len(human)}")

    agent_mat = compute_corr_matrix(agent, agent_cols)
    human_mat = compute_corr_matrix(human, human_cols)

    plot_heatmap(agent_mat, agent_labels,
                 "Spearman Rank Correlation Matrix: Agent PRs", OUT_AGENT)
    plot_heatmap(human_mat, human_labels,
                 "Spearman Rank Correlation Matrix: Human PRs", OUT_HUMAN)

    print("\n[DONE] Both heatmaps saved.")

if __name__ == "__main__":
    main()
