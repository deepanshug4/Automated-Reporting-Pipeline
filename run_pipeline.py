"""
Automated Reporting Pipeline — entry point.

Run manually:
    python run_pipeline.py

Run automatically (unattended): schedule this with cron or GitHub Actions
(see README). This single command does the full extract -> validate ->
transform -> report flow and exits with a non-zero code on failure, so a
scheduler can detect problems.
"""

import sys
import logging

from src.extract import extract
from src.validate import validate
from src.transform import transform
from src.report import build_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("pipeline")


def main() -> int:
    logger.info("=== Pipeline run started ===")

    df = extract()

    is_valid, issues = validate(df)
    if not is_valid:
        logger.error("Aborting: data failed validation:")
        for i in issues:
            logger.error("  - %s", i)
        return 1  # non-zero => scheduler sees failure

    metrics = transform(df)
    result = build_report(metrics)

    if result["alert"]:
        logger.warning("ALERT: %s", result["alert"])

    logger.info("Report ready: %s", result["html_path"])
    logger.info("=== Pipeline run finished ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())