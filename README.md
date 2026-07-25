# 📊 Automated Reporting Pipeline

An end-to-end data pipeline that **extracts** data, **validates** it,
**computes business metrics**, and **generates a report automatically** —
designed to run unattended on a schedule.

📸 
<img width="1783" height="706" alt="image" src="https://github.com/user-attachments/assets/9843e2b7-24e7-44db-9c37-a5052578e74f" />
<img width="1783" height="706" alt="image" src="https://github.com/user-attachments/assets/5586d35e-cb4b-477c-a7a1-fc979c3e5cae" />


## The problem
Teams waste hours each week manually pulling data and rebuilding the same
reports. Manual reporting is slow, inconsistent, and easy to get wrong.

## What it does
`extract → validate → transform → report`, as a single headless command:

- **Extract** — pulls data from a source (with a CSV fallback for resilience).
- **Validate** — a data-quality gate: missing columns, excessive nulls,
  non-numeric or negative values. The pipeline **fails loudly** on bad data
  instead of producing a wrong report.
- **Transform** — computes revenue/units by period, region, and product, and
  period-over-period change.
- **Report** — renders a self-contained **HTML report** + a machine-readable
  CSV summary, with **timestamped filenames** so every run is auditable.
- **Alerting** — flags when revenue drops beyond a configurable threshold.

A separate **Streamlit dashboard** displays the latest report.

## Why it's built this way
- The pipeline is a **headless script** (`run_pipeline.py`), not a UI — because
  real reporting runs unattended. It exits non-zero on failure so a scheduler
  can detect problems.
- **Logging, validation, config-driven thresholds, and timestamped outputs**
  reflect production practice, not a one-off script.

## Run it
```bash
pip install -r requirements.txt
python run_pipeline.py          # generates a report in output/
streamlit run dashboard.py      # view the latest report
