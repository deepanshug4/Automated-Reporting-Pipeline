"""
Central configuration. Keeping paths, thresholds, and settings in one place
(instead of scattered/hardcoded) is a small thing that signals production
discipline — anyone can change behavior without hunting through code.
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Data source
SAMPLE_CSV = DATA_DIR / "sample_sales.csv"
# A no-auth public endpoint could go here; we default to CSV for reliability.
USE_REMOTE = False
REMOTE_URL = ""  # e.g. a public CSV/JSON endpoint if you want a live source

# Validation thresholds
REQUIRED_COLUMNS = ["date", "region", "product", "units", "revenue"]
MAX_NULL_FRACTION = 0.10   # fail if >10% of a required column is null

# Business thresholds (used to flag insights in the report)
REVENUE_ALERT_DROP_PCT = 15.0  # flag if latest period drops >15% vs prior

OUTPUT_DIR.mkdir(exist_ok=True)