"""
Dashboard to VIEW the latest pipeline output. This is separate from the
pipeline itself (which runs headless). Run:  streamlit run dashboard.py
"""

import glob
import os
import pandas as pd
import streamlit as st

from config import OUTPUT_DIR

st.set_page_config(page_title="Reporting Pipeline Dashboard", layout="wide")
st.title("📊 Automated Reporting Pipeline — Dashboard")
st.caption("Views the latest report produced by run_pipeline.py")

summaries = sorted(glob.glob(str(OUTPUT_DIR / "summary_*.csv")))
reports = sorted(glob.glob(str(OUTPUT_DIR / "report_*.html")))

if not summaries:
    st.info("No reports yet. Run `python run_pipeline.py` first.")
else:
    latest_summary = pd.read_csv(summaries[-1])
    row = latest_summary.iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${row['total_revenue']:,.2f}")
    c2.metric("Total Units", int(row["total_units"]))
    if pd.notna(row["latest_pct_change"]):
        c3.metric("Latest Period Change", f"{row['latest_pct_change']:.1f}%")

    if isinstance(row["alert"], str) and row["alert"]:
        st.error(f"⚠️ {row['alert']}")
    else:
        st.success("✅ No revenue-drop alerts.")

    if reports:
        with open(reports[-1], "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=800, scrolling=True)

    st.caption(f"Showing latest of {len(summaries)} report(s).")