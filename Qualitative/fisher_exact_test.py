"""
Fisher's Exact Test: Documentation/Content Bloat vs. other Scope Creep subcategories
Comparing AI agent-generated vs. human-authored revert PRs

Research context:
    Tests whether Documentation/Content Bloat is proportionally more common
    in human Scope Creep reverts than in AI Scope Creep reverts, despite the
    small human sample size (n=40).

Contingency table:
                        | Doc/Content Bloat | All other Scope Creep subcategories |
    AI agent PRs        |        14         |               143                   |
    Human developer PRs |         9         |                31                   |

Result: Fisher's exact test p = 0.026, odds ratio = 0.337
    -> The difference is statistically significant at alpha = 0.05
    -> Human Scope Creep reverts are proportionally more likely to involve
       Documentation/Content Bloat than AI Scope Creep reverts.
"""

from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint
import numpy as np

# --- Data ---
# AI:    14 of 157 Scope Creep reverts coded as Documentation/Content Bloat
# Human:  9 of 40  Scope Creep reverts coded as Documentation/Content Bloat
ai_bloat      = 14
ai_total      = 157
human_bloat   = 9
human_total   = 40

ai_other    = ai_total    - ai_bloat
human_other = human_total - human_bloat

# --- Contingency table ---
# Rows: [AI, Human]
# Cols: [Documentation/Content Bloat, All other subcategories]
table = np.array([
    [ai_bloat,    ai_other],
    [human_bloat, human_other]
])

print("Contingency table:")
print(f"                     | Doc/Content Bloat | Other subcategories |")
print(f"  AI agent PRs       |        {ai_bloat:>2}         |         {ai_other:>3}         |")
print(f"  Human developer PRs|        {human_bloat:>2}         |          {human_other:>2}         |")
print()

# --- Fisher's exact test ---
odds_ratio, p_value = fisher_exact(table)

print(f"Fisher's exact test:")
print(f"  Odds ratio = {odds_ratio:.3f}")
print(f"  p-value    = {p_value:.3f}")
print(f"  Significant at alpha=0.05: {p_value < 0.05}")
print()

# --- Proportions with Wilson confidence intervals ---
ai_prop    = ai_bloat    / ai_total
human_prop = human_bloat / human_total

ai_ci    = proportion_confint(ai_bloat,    ai_total,    method='wilson')
human_ci = proportion_confint(human_bloat, human_total, method='wilson')

print(f"Proportions (Wilson 95% CI):")
print(f"  AI agent PRs:       {ai_prop:.3f}  [{ai_ci[0]:.3f}, {ai_ci[1]:.3f}]")
print(f"  Human developer PRs:{human_prop:.3f}  [{human_ci[0]:.3f}, {human_ci[1]:.3f}]")
print()
print("Interpretation:")
print(f"  Documentation/Content Bloat is proportionally more common in human")
print(f"  Scope Creep reverts ({human_prop*100:.1f}%) than in AI Scope Creep reverts")
print(f"  ({ai_prop*100:.1f}%). This difference is statistically significant")
print(f"  (Fisher's exact p = {p_value:.3f}) despite the small human sample (n={human_total}).")
