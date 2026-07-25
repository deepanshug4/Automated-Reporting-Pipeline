"""
Validation gate: refuse to build a report on bad data. A pipeline that
silently reports on broken data is worse than one that fails loudly.
Returns (is_valid, list_of_issues).
"""

import logging
import pandas as pd

from config import REQUIRED_COLUMNS, MAX_NULL_FRACTION

logger = logging.getLogger(__name__)


def validate(df: pd.DataFrame) -> tuple[bool, list[str]]:
    issues = []

    # Required columns present?
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        issues.append(f"Missing required columns: {missing}")
        return False, issues  # can't check further

    # Null fractions
    for col in REQUIRED_COLUMNS:
        null_frac = df[col].isna().mean()
        if null_frac > MAX_NULL_FRACTION:
            issues.append(
                f"Column '{col}' is {null_frac:.0%} null "
                f"(threshold {MAX_NULL_FRACTION:.0%})."
            )

    # Numeric sanity
    for col in ["units", "revenue"]:
        coerced = pd.to_numeric(df[col], errors="coerce")
        if coerced.isna().any():
            issues.append(f"Column '{col}' contains non-numeric values.")
        if (coerced < 0).any():
            issues.append(f"Column '{col}' contains negative values.")

    is_valid = len(issues) == 0
    if is_valid:
        logger.info("Validation passed.")
    else:
        logger.warning("Validation found %d issue(s).", len(issues))
    return is_valid, issues