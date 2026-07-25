"""
Extract step: fetch raw data. Uses a remote source if configured, otherwise
falls back to a local CSV so the pipeline ALWAYS runs (important for a demo
and for resilience — real pipelines need a fallback path).
"""

import logging
import pandas as pd
import requests

from config import USE_REMOTE, REMOTE_URL, SAMPLE_CSV

logger = logging.getLogger(__name__)


def extract() -> pd.DataFrame:
    if USE_REMOTE and REMOTE_URL:
        try:
            logger.info("Fetching data from remote source: %s", REMOTE_URL)
            resp = requests.get(REMOTE_URL, timeout=30)
            resp.raise_for_status()
            from io import StringIO
            df = pd.read_csv(StringIO(resp.text))
            logger.info("Fetched %d rows from remote.", len(df))
            return df
        except Exception as e:
            logger.warning("Remote fetch failed (%s). Falling back to CSV.", e)

    logger.info("Loading data from local CSV: %s", SAMPLE_CSV)
    df = pd.read_csv(SAMPLE_CSV)
    logger.info("Loaded %d rows from CSV.", len(df))
    return df