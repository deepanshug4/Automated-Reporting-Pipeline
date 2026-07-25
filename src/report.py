"""
Report step: render metrics into a self-contained HTML artifact and save a
machine-readable CSV summary. Timestamped filenames make every run
traceable/auditable — you can always see what was reported and when.
"""

import logging
from datetime import datetime
import pandas as pd
from jinja2 import Template

from config import OUTPUT_DIR, REVENUE_ALERT_DROP_PCT

logger = logging.getLogger(__name__)

_HTML = Template("""
<html><head><meta charset="utf-8"><title>Sales Report</title>
<style>
 body{font-family:Arial,sans-serif;margin:40px;color:#222}
 h1{margin-bottom:0} .sub{color:#666}
 .kpi{display:inline-block;padding:16px 24px;margin:8px;border:1px solid #eee;border-radius:8px}
 .kpi .val{font-size:24px;font-weight:bold}
 table{border-collapse:collapse;margin-top:12px} td,th{border:1px solid #ddd;padding:6px 12px}
 .alert{background:#ffe6e6;padding:12px;border-radius:6px;color:#a00}
 .ok{background:#e6ffed;padding:12px;border-radius:6px;color:#070}
</style></head><body>
<h1>Automated Sales Report</h1>
<div class="sub">Generated {{ generated_at }}</div>

{% if alert %}<p class="alert">⚠️ {{ alert }}</p>
{% else %}<p class="ok">✅ No revenue-drop alerts this period.</p>{% endif %}

<div>
 <div class="kpi"><div>Total Revenue</div><div class="val">${{ '%.2f'|format(total_revenue) }}</div></div>
 <div class="kpi"><div>Total Units</div><div class="val">{{ total_units }}</div></div>
 {% if pct_change is not none %}
 <div class="kpi"><div>Latest Period Change</div><div class="val">{{ '%.1f'|format(pct_change) }}%</div></div>
 {% endif %}
</div>

<h3>Revenue by Period</h3>{{ by_period }}
<h3>Revenue by Region</h3>{{ by_region }}
<h3>Revenue by Product</h3>{{ by_product }}
</body></html>
""")


def build_report(metrics: dict) -> dict:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    alert = None
    pct = metrics["latest_pct_change"]
    if pct is not None and pct <= -REVENUE_ALERT_DROP_PCT:
        alert = (f"Revenue fell {abs(pct):.1f}% in the latest period "
                 f"(threshold {REVENUE_ALERT_DROP_PCT:.0f}%).")

    html = _HTML.render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_revenue=metrics["total_revenue"],
        total_units=metrics["total_units"],
        pct_change=pct,
        alert=alert,
        by_period=metrics["by_period"].to_html(index=False),
        by_region=metrics["by_region"].to_html(index=False),
        by_product=metrics["by_product"].to_html(index=False),
    )

    html_path = OUTPUT_DIR / f"report_{ts}.html"
    html_path.write_text(html, encoding="utf-8")

    # Machine-readable summary (for downstream use / the dashboard).
    summary_path = OUTPUT_DIR / f"summary_{ts}.csv"
    pd.DataFrame([{
        "generated_at": ts,
        "total_revenue": metrics["total_revenue"],
        "total_units": metrics["total_units"],
        "latest_pct_change": pct,
        "alert": alert or "",
    }]).to_csv(summary_path, index=False)

    logger.info("Report written: %s", html_path)
    return {"html_path": str(html_path), "summary_path": str(summary_path),
            "alert": alert}