"""
Fisher's Exact Test: Reviewer Activity in AI Agent vs. Human Revert PRs

Research context:
    Tests whether the presence of reviewer activity differs significantly
    between AI agent-generated and human-authored revert PRs.

Contingency table:
                        | With reviewer activity | Without reviewer activity |
    AI agent PRs        |          36            |           806             |
    Human developer PRs |         625            |           295             |

Result: Fisher's exact test p = 1.66e-192, odds ratio = 0.021
    -> The difference is statistically significant at any conventional alpha.
    -> AI agent PRs are overwhelmingly less likely to receive reviewer
       activity than human developer PRs.
"""

from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint
import numpy as np

# --- Data ---
ai_total        = 842
ai_with_review  = 36
hu_total        = 920
hu_with_review  = 625

ai_without = ai_total - ai_with_review
hu_without = hu_total - hu_with_review

# --- Contingency table ---
table = np.array([
    [ai_with_review, ai_without],
    [hu_with_review, hu_without]
])

print("Contingency table:")
print(f"                     | With Review | Without Review |")
print(f"  AI agent PRs       |     {ai_with_review:>3}     |      {ai_without:>3}       |")
print(f"  Human developer PRs|     {hu_with_review:>3}     |      {hu_without:>3}       |")
print()

# --- Fisher's exact test ---
odds_ratio, p_value = fisher_exact(table)
print(f"Fisher's exact test:")
print(f"  Odds ratio = {odds_ratio:.4f}")
print(f"  p-value    = {p_value:.2e}")
print(f"  Significant at alpha=0.05: {p_value < 0.05}")
print()

# --- Proportions with Wilson confidence intervals ---
ai_prop = ai_with_review / ai_total
hu_prop = hu_with_review / hu_total

ai_ci = proportion_confint(ai_with_review, ai_total, method='wilson')
hu_ci = proportion_confint(hu_with_review, hu_total, method='wilson')

print(f"Proportions with reviewer activity (Wilson 95% CI):")
print(f"  AI agent PRs:       {ai_prop:.3f} ({ai_prop*100:.1f}%)  [{ai_ci[0]:.3f}, {ai_ci[1]:.3f}]")
print(f"  Human developer PRs:{hu_prop:.3f} ({hu_prop*100:.1f}%) [{hu_ci[0]:.3f}, {hu_ci[1]:.3f}]")
print()
print("Interpretation:")
print(f"  Only {ai_with_review} of {ai_total} AI agent revert PRs ({ai_prop*100:.1f}%) received any reviewer")
print(f"  activity, compared to {hu_with_review} of {hu_total} human PRs ({hu_prop*100:.1f}%). The difference")
print(f"  is highly significant (Fisher's exact p = {p_value:.2e}), confirming")
print(f"  that AI agent PRs are processed with dramatically less review")
print(f"  engagement than human-authored revert PRs.")
