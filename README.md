# agent-human-revert
# Comparing AI Agent and Human Revert Pull Requests

An empirical study of process, review, and failure modes that compares 842 agent-generated and 920 human-generated revert pull requests on GitHub. We use the Mann-Whitney U test, Cliff's Delta, and a qualitative revert-reason taxonomy.

## Repository Structure

```
├── Quantitative/   — Metrics pipeline: PR data, comparison scripts, statistical results, plots
├── Qualitative/    — Taxonomy coding: revert-reason categories and subcategories 
├── Excel/          — Source datasets (AIDev and human PR ID/metadata files)
└── README.md       — This file
```

Each subfolder has its own README with details specific to that part of the study — see [Quantitative/README.md](Quantitative/README.md), [Qualitative/README.md](Qualitative/README.md), and [Excel/README.md](Excel/README.md).

## Summary

- **Agent dataset**: 842 filtered revert PRs from five AI coding agents (OpenAI Codex, Devin, GitHub Copilot, Cursor, Claude Code), sourced from the AIDev dataset. 841 of these have complete quantitative metrics; one PR's source repository was restricted by GitHub, but it remains part of the qualitative dataset.
- **Human dataset**: 920 filtered revert PRs mined from public GitHub repositories.
- **Quantitative analysis**: acceptance rate, time to close, review iterations, total comments, reviewer workload, code churn, and description length, compared using the Mann-Whitney U test and Cliff's Delta.
- **Qualitative analysis**: a taxonomy of seven revert-reason categories grouped into three failure modes (Technical Correctness, Judgment/Alignment, Process/Integration).

## Paper

The full paper is available at `[link or path to the paper file in this repo]`.
