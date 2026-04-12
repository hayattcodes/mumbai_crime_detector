
import streamlit as st
import pandas as pd
import numpy as np
import plotly.colors
import plotly.graph_objects as go
from typing import Optional

# ── Page config (must be first) ─────────────────────────────────────
st.set_page_config(
    page_title="Mumbai Crime Area Detector",
    page_icon="🏙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════

WARDS = {
    "A":   ("Colaba / Fort",         "Zone I – South"),
    "B":   ("Mazgaon / Dongri",      "Zone I – South"),
    "C":   ("Matunga / Sion",        "Zone II – Central"),
    "D":   ("Malabar Hill",          "Zone I – South"),
    "E":   ("Byculla / Nagpada",     "Zone II – Central"),
    "F/N": ("Matunga East",          "Zone II – Central"),
    "F/S": ("Worli / Prabhadevi",    "Zone II – Central"),
    "G/N": ("Dharavi / Sion",        "Zone II – Central"),
    "G/S": ("Mahim / Dadar",         "Zone II – Central"),
    "H/E": ("Bandra East",           "Zone III – Western Suburbs"),
    "H/W": ("Bandra West",           "Zone III – Western Suburbs"),
    "K/E": ("Andheri East",          "Zone IV – W Suburbs North"),
    "K/W": ("Andheri West",          "Zone IV – W Suburbs North"),
    "L":   ("Kurla",                 "Zone V – Eastern Suburbs"),
    "M/E": ("Chembur East",          "Zone V – Eastern Suburbs"),
    "M/W": ("Chembur West",          "Zone V – Eastern Suburbs"),
    "N":   ("Ghatkopar",             "Zone V – Eastern Suburbs"),
    "P/N": ("Goregaon North",        "Zone IV – W Suburbs North"),
    "P/S": ("Goregaon South",        "Zone IV – W Suburbs North"),
    "R/C": ("Borivali Central",      "Zone VI – North"),
    "R/N": ("Borivali North",        "Zone VI – North"),
    "R/S": ("Borivali South",        "Zone VI – North"),
    "S":   ("Bhandup / Vikhroli",    "Zone VII – North East"),
    "T":   ("Mulund",                "Zone VII – North East"),
}

WARD_COORDS = {
    "A":   (18.906, 72.818), "B":   (18.958, 72.843),
    "C":   (19.020, 72.857), "D":   (18.954, 72.802),
    "E":   (18.978, 72.838), "F/N": (19.035, 72.862),
    "F/S": (19.005, 72.817), "G/N": (19.047, 72.853),
    "G/S": (19.030, 72.840), "H/E": (19.054, 72.868),
    "H/W": (19.059, 72.831), "K/E": (19.113, 72.878),
    "K/W": (19.119, 72.840), "L":   (19.072, 72.880),
    "M/E": (19.062, 72.900), "M/W": (19.048, 72.893),
    "N":   (19.086, 72.908), "P/N": (19.162, 72.850),
    "P/S": (19.149, 72.848), "R/C": (19.225, 72.858),
    "R/N": (19.245, 72.855), "R/S": (19.215, 72.852),
    "S":   (19.147, 72.940), "T":   (19.172, 72.958),
}

CRIME_TYPES = [
    "Theft", "Vehicle Theft", "Robbery", "Burglary",
    "Assault", "Murder", "Kidnapping", "Fraud",
    "Drug Offences", "Eve Teasing",
]

CRIME_MULT = {
    "Theft": 3.2, "Vehicle Theft": 2.6, "Robbery": 1.5,
    "Burglary": 1.3, "Assault": 1.1, "Murder": 0.08,
    "Kidnapping": 0.12, "Fraud": 1.9, "Drug Offences": 0.85,
    "Eve Teasing": 0.72,
}

BASE_RATES = {
    "A": 0.55, "B": 0.82, "C": 0.50, "D": 0.28, "E": 0.92,
    "F/N": 0.60, "F/S": 0.48, "G/N": 1.00, "G/S": 0.72,
    "H/E": 0.68, "H/W": 0.42, "K/E": 0.80, "K/W": 0.52,
    "L": 0.90, "M/E": 0.70, "M/W": 0.62, "N": 0.74,
    "P/N": 0.50, "P/S": 0.58, "R/C": 0.40, "R/N": 0.30,
    "R/S": 0.38, "S": 0.65, "T": 0.48,
}

SAFE_COLOR  = "#2D6A4F"
MOD_COLOR   = "#B45309"
RISK_COLOR  = "#9B1C1C"
NAVY        = "#1E3A5F"
LIGHT_NAVY  = "#E8EFF7"

# ═══════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: #F7F7F5 !important;
}
.block-container { padding: 2.5rem 2.8rem 3rem !important; max-width: 1440px !important; }
header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }

/* ── App header ── */
.app-header { padding-bottom: 28px; border-bottom: 1px solid #E8E8E4; margin-bottom: 24px; display:flex; justify-content:space-between; align-items:flex-start; }
.app-eyebrow { font-size:11px; font-weight:700; letter-spacing:.10em; text-transform:uppercase; color:#ABABAA; margin-bottom:8px; }
.app-title   { font-family:'Sora',sans-serif; font-size:28px; font-weight:800; color:#1A1A18; letter-spacing:-0.04em; line-height:1; margin:0; }
.app-sub     { font-size:13px; color:#8A8A80; margin-top:7px; }
.app-badge   { background:#1E3A5F; color:#fff; padding:6px 14px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:.05em; display:inline-block; white-space:nowrap; }

/* ── KPI cards ── */
.kpi-card  { background:#fff; border-radius:14px; padding:20px 18px 16px; border:1px solid #EBEBEA; box-shadow:0 1px 4px rgba(0,0,0,.04); height:100%; }
.kpi-card-interactive { cursor:pointer; transition: box-shadow .15s, border-color .15s; }
.kpi-card-interactive:hover { box-shadow:0 4px 14px rgba(30,58,95,.10); border-color:#BDD0E8; }
.kpi-eye   { font-size:10px; font-weight:700; color:#ABABAA; letter-spacing:.10em; text-transform:uppercase; margin-bottom:8px; }
.kpi-num   { font-family:'Sora',sans-serif; font-size:30px; font-weight:800; color:#1A1A18; line-height:1; letter-spacing:-0.04em; }
.kpi-desc  { font-size:12px; color:#8A8A80; margin-top:6px; line-height:1.4; }
.kpi-cta   { font-size:11px; font-weight:600; color:#1E3A5F; margin-top:10px; opacity:.7; }

/* Ghost explore button inside KPI card column */
div[data-testid="stButton"].kpi-btn > button {
    background: transparent !important;
    border: 1px solid #DDEAF5 !important;
    color: #1E3A5F !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    padding: 3px 10px !important;
    border-radius: 8px !important;
    margin-top: 8px !important;
    width: 100% !important;
    letter-spacing: .02em !important;
}
div[data-testid="stButton"].kpi-btn > button:hover {
    background: #EEF4FB !important;
    border-color: #A8C4DE !important;
}

/* ── Panel wrapper ── */
.panel     { background:#fff; border-radius:16px; border:1px solid #EBEBEA; box-shadow:0 1px 6px rgba(0,0,0,.05); overflow:hidden; }
.panel-hdr { padding:16px 20px 12px; border-bottom:1px solid #F2F2F0; }
.panel-ttl { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#1A1A18; letter-spacing:-0.02em; margin:0; }
.panel-sub { font-size:11px; color:#ABABAA; margin:2px 0 0; }
.panel-bod { padding:20px 20px; overflow-y:auto; max-height:560px; }

/* ── Map affordance hint ── */
.map-hint {
    font-size:11px; color:#ABABAA; text-align:center;
    padding:7px 0 4px; letter-spacing:.02em;
    display:flex; align-items:center; justify-content:center; gap:5px;
}
.map-hint-dot { width:8px; height:8px; background:#1E3A5F; border-radius:50%; opacity:.35; display:inline-block; }

/* ── Status pills ── */
.pill      { display:inline-flex; align-items:center; gap:4px; padding:4px 11px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:.03em; }
.pill-safe { background:#D1FAE5; color:#065F46; }
.pill-mod  { background:#FEF3C7; color:#92400E; }
.pill-risk { background:#FEE2E2; color:#991B1B; }

/* ── Ward score block ── */
.score-wrap  { display:flex; align-items:baseline; gap:5px; margin:14px 0 10px; }
.score-num   { font-family:'Sora',sans-serif; font-size:58px; font-weight:800; line-height:1; letter-spacing:-0.05em; }
.score-denom { font-size:20px; color:#ABABAA; }
.score-safe  { color:#2D6A4F; }
.score-mod   { color:#B45309; }
.score-risk  { color:#9B1C1C; }

/* ── Stats rows ── */
.stat-row   { display:flex; justify-content:space-between; padding:9px 0; border-bottom:1px solid #F7F7F5; }
.stat-lbl   { font-size:12px; color:#8A8A80; }
.stat-val   { font-size:12px; font-weight:600; color:#1A1A18; }

/* ── Crime bars (with % column) ── */
.cbar-row   { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.cbar-lbl   { font-size:11px; color:#6B6B63; width:96px; flex-shrink:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.cbar-track { flex:1; height:5px; background:#F0F0EE; border-radius:3px; overflow:hidden; }
.cbar-fill  { height:100%; border-radius:3px; background:#1E3A5F; }
.cbar-pct   { font-size:11px; color:#1E3A5F; font-weight:600; width:30px; text-align:right; flex-shrink:0; }
.cbar-cnt   { font-size:11px; color:#ABABAA; width:44px; text-align:right; flex-shrink:0; }

/* ── Section label ── */
.section-lbl { font-size:10px; font-weight:700; color:#ABABAA; letter-spacing:.08em; text-transform:uppercase; margin:0 2px 10px; }

/* ── Empty state ── */
.empty-state { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:400px; gap:10px; text-align:center; }
.empty-icon  { font-size:36px; opacity:.4; }
.empty-title { font-family:'Sora',sans-serif; font-size:15px; font-weight:600; color:#8A8A80; letter-spacing:-0.02em; }
.empty-sub   { font-size:12px; color:#ABABAA; line-height:1.8; max-width:240px; }
.empty-ways  { display:flex; flex-direction:column; gap:6px; margin-top:4px; }
.empty-way   { background:#F4F4F2; border-radius:8px; padding:6px 14px; font-size:11px; color:#8A8A80; display:inline-block; }

/* ── Prediction banner ── */
.pred-banner { background:#EEF2F8; border-radius:12px; padding:16px 18px; display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
.pred-lbl    { font-size:10px; font-weight:700; color:#5A6A7A; letter-spacing:.08em; text-transform:uppercase; margin-bottom:4px; }
.pred-val    { font-family:'Sora',sans-serif; font-size:26px; font-weight:800; color:#1E3A5F; letter-spacing:-0.04em; }

/* ── Tab 2 context banner ── */
.tab-banner     { background:#EEF2F8; border-radius:10px; padding:10px 16px; margin-bottom:18px; display:flex; align-items:center; gap:8px; }
.tab-banner-ico { font-size:14px; }
.tab-banner-txt { font-size:12px; font-weight:600; color:#1E3A5F; }
.tab-banner-sub { font-size:11px; color:#7A8FA0; margin-left:4px; font-weight:400; }

/* ── Rank table rows ── */
.rank-row    { display:flex; align-items:center; gap:10px; padding:9px 0; border-bottom:1px solid #F7F7F5; }
.rank-n      { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#DADADA; width:22px; }
.rank-name   { font-size:13px; color:#1A1A18; flex:1; }
.rank-ward   { font-size:11px; color:#ABABAA; margin-right:auto; }
.rank-score  { font-family:'Sora',sans-serif; font-size:13px; font-weight:700; }

/* ── Divider ── */
.sep { height:1px; background:#EBEBEA; margin:28px 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background:#F0F0EE; border-radius:10px; padding:4px; gap:2px; }
.stTabs [data-baseweb="tab"] { border-radius:7px; padding:7px 18px; font-size:13px; font-weight:500; color:#8A8A80; border:none; }
.stTabs [aria-selected="true"] { background:#fff !important; color:#1A1A18 !important; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,.08); }
.stTabs [data-baseweb="tab-panel"] { padding-top:20px !important; }

/* ── Selectbox ── */
div[data-testid="stSelectbox"] label {
    font-size:11px !important; font-weight:700 !important;
    color:#ABABAA !important; text-transform:uppercase !important;
    letter-spacing:.07em !important;
}
</style>
"""

# ═══════════════════════════════════════════════════════════════════
#  DATA GENERATION
# ═══════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner="Loading Mumbai crime data…")
def load_data() -> pd.DataFrame:
    np.random.seed(2024)
    rows = []
    for ward, (area, zone) in WARDS.items():
        for year in range(2020, 2025):
            for month in range(1, 13):
                for crime in CRIME_TYPES:
                    lam = BASE_RATES[ward] * CRIME_MULT[crime] * 9
                    rows.append({
                        "Ward": ward, "Area": area, "Zone": zone,
                        "Year": year, "Month": month,
                        "Crime_Type": crime,
                        "Cases": int(np.random.poisson(max(lam, 0.1))),
                    })
    return pd.DataFrame(rows)

# ═══════════════════════════════════════════════════════════════════
#  ANALYSER
# ═══════════════════════════════════════════════════════════════════

class CrimeAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.scores = self._scores()

    def _scores(self):
        t = self.df.groupby("Ward")["Cases"].sum()
        lo, hi = t.min(), t.max()
        return {w: round(100 - (v - lo) / (hi - lo) * 100, 1) for w, v in t.items()}

    def ward_info(self, ward: str) -> dict:
        d = self.df[self.df["Ward"] == ward]
        area, zone = WARDS[ward]
        return {
            "ward": ward, "area": area, "zone": zone,
            "total": int(d["Cases"].sum()),
            "score": self.scores[ward],
            "breakdown": d.groupby("Crime_Type")["Cases"].sum().sort_values(ascending=False),
            "yearly":    d.groupby("Year")["Cases"].sum(),
            "monthly":   d.groupby("Month")["Cases"].mean(),
        }

    def zone_summary(self): return self.df.groupby("Zone")["Cases"].sum().sort_values(ascending=False)
    def top_danger(self, n=10): return self.df.groupby(["Ward","Area"])["Cases"].sum().sort_values(ascending=False).head(n)
    def safest(self, n=5):   return sorted(self.scores.items(), key=lambda x: -x[1])[:n]
    def riskiest(self, n=5): return sorted(self.scores.items(), key=lambda x:  x[1])[:n]


@st.cache_data
def get_analyzer(df: pd.DataFrame) -> CrimeAnalyzer:
    return CrimeAnalyzer(df)

# ═══════════════════════════════════════════════════════════════════
#  PREDICTION
# ═══════════════════════════════════════════════════════════════════

def predict_2025(yearly: pd.Series):
    """OLS linear regression → predict 2025 with 95% CI."""
    years  = np.array(yearly.index, dtype=float)
    values = np.array(yearly.values, dtype=float)
    ym     = years.mean()
    yc     = years - ym
    coeffs = np.polyfit(yc, values, 1)
    slope, _ = coeffs
    pred   = slope * (2025 - ym) + coeffs[1]
    fitted = np.polyval(coeffs, yc)
    resid  = values - fitted
    n      = len(years)
    se     = np.sqrt(np.sum(resid**2) / max(n - 2, 1))
    x_new  = 2025 - ym
    se_p   = se * np.sqrt(1 + 1/n + x_new**2 / max(np.sum(yc**2), 1e-9))
    ss_res = np.sum(resid**2)
    ss_tot = np.sum((values - values.mean())**2)
    r2     = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return max(0, pred), se_p * 2.0, slope, r2

# ═══════════════════════════════════════════════════════════════════
#  CHART BUILDERS
# ═══════════════════════════════════════════════════════════════════

PLOTLY_BASE = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="DM Sans", font_color="#2A2A22",
)

def _axis_style(**kw):
    defaults = dict(
        showgrid=True, gridcolor="#E0E0DC", gridwidth=1,
        zeroline=False,
        tickfont=dict(size=11, color="#2A2A22"),   # dark, readable tick labels
        title_font=dict(size=11, color="#2A2A22"), # dark axis title
        linecolor="#C8C8C4",
        tickcolor="#6A6A62",
    )
    defaults.update(kw)
    return defaults


def build_sparkline(yearly: pd.Series) -> go.Figure:
    """Tiny inline trend line for the detail panel."""
    years  = list(yearly.index)
    vals   = list(yearly.values)
    pred, _, slope, _ = predict_2025(yearly)
    line_color = RISK_COLOR if slope > 0 else SAFE_COLOR

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=vals, mode="lines+markers",
        line=dict(color=line_color, width=2.5),
        marker=dict(size=5, color=line_color),
        hovertemplate="%{x}: <b>%{y:,}</b><extra></extra>",
    ))
    # 2025 forecast point
    fig.add_trace(go.Scatter(
        x=[2025], y=[pred], mode="markers",
        marker=dict(size=8, color="#C1440E", symbol="diamond"),
        hovertemplate=f"2025 est: <b>{pred:,.0f}</b><extra></extra>",
        showlegend=False,
    ))
    fig.update_layout(
        height=72, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def build_map(az: CrimeAnalyzer, selected: Optional[str] = None) -> go.Figure:
    """Uses go.Scattermapbox directly — avoids px.scatter_mapbox deprecation issues."""
    totals = az.df.groupby("Ward")["Cases"].sum()

    def score_to_color(sc):
        if sc < 40:   return "#9B1C1C"
        elif sc < 60: return "#B45309"
        elif sc < 75: return "#2D6A4F"
        else:         return "#059669"

    lats, lons, texts, colors, sizes, customdata = [], [], [], [], [], []
    total_max = max(int(totals[w]) for w in WARDS)

    for w, (area, zone) in WARDS.items():
        lat, lon = WARD_COORDS[w]
        sc  = az.scores[w]
        tot = int(totals[w])
        lats.append(lat)
        lons.append(lon)
        texts.append(
            f"<b>Ward {w} · {area}</b><br>"
            f"Safety Score: <b>{sc:.0f}/100</b><br>"
            f"Total Cases: {tot:,}<br>"
            f"Zone: {zone}"
        )
        colors.append(score_to_color(sc))
        sizes.append(10 + int(24 * tot / total_max))
        customdata.append([w, sc, tot, zone])

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=lats, lon=lons,
        mode="markers",
        marker=dict(color=colors, size=sizes, opacity=0.88),
        text=texts,
        hovertemplate="%{text}<extra></extra>",
        customdata=customdata,
        showlegend=False,
    ))

    if selected and selected in WARD_COORDS:
        lat, lon = WARD_COORDS[selected]
        fig.add_trace(go.Scattermapbox(
            lat=[lat], lon=[lon], mode="markers",
            marker=dict(size=52, color=NAVY, opacity=0.15),
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scattermapbox(
            lat=[lat], lon=[lon], mode="markers+text",
            marker=dict(size=14, color=NAVY),
            text=[f"Ward {selected}"], textposition="top right",
            textfont=dict(size=11, color=NAVY, family="Sora"),
            hoverinfo="skip", showlegend=False,
        ))

    fig.update_layout(
        height=490,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        mapbox=dict(
            style="carto-positron",
            zoom=10.2,
            center=dict(lat=19.076, lon=72.877),
        ),
    )
    return fig
def build_trend_chart(info: dict) -> tuple:
    yearly      = info["yearly"]
    pred, ci, slope, _ = predict_2025(yearly)
    yrs_actual  = list(yearly.index)
    vals_actual = list(yearly.values)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=yrs_actual, y=vals_actual, name="Actual",
        marker_color=NAVY, marker_opacity=0.82,
        width=0.45, hovertemplate="%{x}: <b>%{y:,}</b><extra></extra>",
    ))

    fig.add_trace(go.Bar(
        x=[2025], y=[pred], name="2025 Forecast",
        marker_color="#C1440E", marker_opacity=0.75,
        width=0.45,
        error_y=dict(type="data", array=[ci], visible=True,
                     color="#C1440E", thickness=1.5, width=5),
        hovertemplate=(
            f"2025 Forecast: <b>{pred:,.0f}</b><br>"
            f"Range: {max(0,pred-ci):,.0f} – {pred+ci:,.0f}<extra></extra>"
        ),
    ))

    all_yrs = np.array(yrs_actual + [2025], dtype=float)
    ym      = np.mean(yrs_actual)
    c       = np.polyfit(np.array(yrs_actual) - ym, vals_actual, 1)
    trend   = np.polyval(c, all_yrs - ym)
    fig.add_trace(go.Scatter(
        x=all_yrs, y=trend, mode="lines", name="Trend",
        line=dict(color="#ABABAA", width=1.4, dash="dot"),
        hoverinfo="skip",
    ))

    fig.update_layout(
        **PLOTLY_BASE, height=260, margin=dict(l=4, r=4, t=8, b=4),
        bargap=0.3, barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font_size=11),
        xaxis=_axis_style(showgrid=False,
                          tickvals=yrs_actual + [2025],
                          ticktext=[str(y) for y in yrs_actual] + ["2025 ▸"]),
        yaxis=_axis_style(title="Total Cases"),
    )
    return fig, pred, ci, slope


def build_city_trend(az: CrimeAnalyzer) -> go.Figure:
    zt  = az.df.groupby(["Zone", "Year"])["Cases"].sum().reset_index()
    pal = plotly.colors.qualitative.Pastel
    fig = go.Figure()
    for i, (zone, grp) in enumerate(zt.groupby("Zone")):
        lbl = zone.split("–")[1].strip() if "–" in zone else zone
        fig.add_trace(go.Scatter(
            x=grp["Year"], y=grp["Cases"], mode="lines+markers",
            name=lbl, line=dict(color=pal[i % len(pal)], width=2),
            marker=dict(size=6),
            hovertemplate=f"{lbl} %{{x}}: <b>%{{y:,}}</b><extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_BASE, height=320, margin=dict(l=4, r=4, t=8, b=4),
        xaxis=_axis_style(showgrid=False, tickvals=list(range(2020, 2025))),
        yaxis=_axis_style(title="Total Cases"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font_size=11),
    )
    return fig


def build_heatmap(az: CrimeAnalyzer) -> go.Figure:
    pivot = az.df.groupby(["Area", "Crime_Type"])["Cases"].sum().unstack(fill_value=0)
    fig   = go.Figure(go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[
            [0.0, "#F9FAFB"], [0.3, "#FEF3C7"],
            [0.6, "#FCA5A5"], [1.0, "#7F1D1D"],
        ],
        hoverongaps=False,
        hovertemplate="%{y}<br>%{x}: <b>%{z:,}</b><extra></extra>",
        colorbar=dict(
            title="Cases", thickness=10, len=0.5,
            tickfont=dict(size=10, color="#2A2A22"),
            title_font=dict(size=11, color="#2A2A22"),
        ),
        xgap=2, ygap=2,
    ))
    fig.update_layout(
        **PLOTLY_BASE,
        height=680,
        xaxis=dict(tickfont=dict(size=11, color="#2A2A22"), tickangle=-35, side="bottom"),
        yaxis=dict(tickfont=dict(size=10, color="#2A2A22"), autorange="reversed"),
        margin=dict(l=150, r=20, t=10, b=80),
    )
    return fig


def build_zone_bars(az: CrimeAnalyzer) -> go.Figure:
    zs    = az.zone_summary()
    short = [z.split("–")[1].strip() if "–" in z else z for z in zs.index]
    total = zs.sum()
    fig   = go.Figure(go.Bar(
        x=zs.values, y=short, orientation="h",
        marker=dict(
            color=zs.values,
            colorscale=[[0, "#D1FAE5"], [0.5, "#FEF3C7"], [1, "#FEE2E2"]],
            showscale=False, line_width=0,
        ),
        text=[f"{v/total*100:.1f}%" for v in zs.values],
        textposition="outside",
        textfont=dict(size=11, color="#2A2A22"),
        hovertemplate="%{y}: <b>%{x:,}</b> cases<extra></extra>",
        width=0.6,
    ))
    fig.update_layout(
        **PLOTLY_BASE, height=300,
        xaxis=_axis_style(title="Total Cases"),
        yaxis=dict(tickfont=dict(size=11, color="#2A2A22"), autorange="reversed"),
        margin=dict(l=130, r=60, t=8, b=8),
    )
    return fig


def build_crime_donut(az: CrimeAnalyzer) -> go.Figure:
    ct  = az.df.groupby("Crime_Type")["Cases"].sum().sort_values(ascending=False)
    pal = [NAVY, "#2D4D8A", "#6B8FBF", "#9FB8D8",
           "#2D6A4F", "#74B49B", "#B45309", "#C1440E",
           "#D97706", "#ABABAA"]
    fig = go.Figure(go.Pie(
        labels=ct.index, values=ct.values,
        hole=0.55,
        marker=dict(colors=pal[:len(ct)], line=dict(color="white", width=2)),
        hovertemplate="%{label}: <b>%{value:,}</b> (%{percent})<extra></extra>",
        textinfo="none",
        sort=False,
    ))
    fig.add_annotation(
        text="Crime<br>Types", x=0.5, y=0.5,
        showarrow=False, font=dict(size=13, color="#8A8A80", family="DM Sans"),
    )
    fig.update_layout(
        **PLOTLY_BASE, height=300,
        legend=dict(font_size=11, orientation="v", x=1.02, y=0.5, yanchor="middle"),
        margin=dict(l=0, r=120, t=8, b=8),
    )
    return fig

# ═══════════════════════════════════════════════════════════════════
#  HTML HELPERS
# ═══════════════════════════════════════════════════════════════════

def _pill(score):
    if score >= 70: return '<span class="pill pill-safe">✓ Safe</span>'
    if score >= 40: return '<span class="pill pill-mod">⚠ Moderate</span>'
    return '<span class="pill pill-risk">✕ High Risk</span>'

def _score_cls(score):
    return "score-safe" if score >= 70 else ("score-mod" if score >= 40 else "score-risk")

def _crime_bars(breakdown: pd.Series, top_n=6) -> str:
    """Render horizontal bars with both % of total and absolute count."""
    top   = breakdown.head(top_n)
    mx    = top.max()
    total = breakdown.sum()
    out   = ""
    for crime, cnt in top.items():
        pct_bar   = cnt / mx * 100
        pct_total = cnt / total * 100 if total > 0 else 0
        out += f"""
        <div class="cbar-row">
          <span class="cbar-lbl">{crime}</span>
          <div class="cbar-track"><div class="cbar-fill" style="width:{pct_bar:.0f}%"></div></div>
          <span class="cbar-pct">{pct_total:.0f}%</span>
          <span class="cbar-cnt">{cnt:,}</span>
        </div>"""
    return out

def _stat(label, value):
    return f'<div class="stat-row"><span class="stat-lbl">{label}</span><span class="stat-val">{value}</span></div>'

def _rank_row(n, ward, area, score):
    col = SAFE_COLOR if score >= 70 else (MOD_COLOR if score >= 40 else RISK_COLOR)
    return f"""
    <div class="rank-row">
      <span class="rank-n">#{n}</span>
      <div style="flex:1">
        <div class="rank-name">{area}</div>
        <div class="rank-ward">Ward {ward}</div>
      </div>
      <span class="rank-score" style="color:{col}">{score:.0f}</span>
    </div>"""

# ═══════════════════════════════════════════════════════════════════
#  PAGE SECTIONS
# ═══════════════════════════════════════════════════════════════════

def render_header(az: CrimeAnalyzer):
    avg   = round(sum(az.scores.values()) / len(az.scores), 1)
    total = az.df["Cases"].sum()
    st.markdown(f"""
    <div class="app-header">
      <div>
        <div class="app-eyebrow">Mumbai  ·  Public Safety Intelligence</div>
        <div class="app-title">Crime Area Detector</div>
        <div class="app-sub">
          Ward-wise analysis across 24 Mumbai wards  ·  2020–2024 data
          &nbsp;&nbsp;|&nbsp;&nbsp; {total:,} records  ·  City avg safety {avg}/100
        </div>
      </div>
      <span class="app-badge">Live Dashboard</span>
    </div>
    """, unsafe_allow_html=True)


def render_kpis(az: CrimeAnalyzer):
    """KPI row — Safest and Riskiest cards are interactive (select ward on click)."""
    total = az.df["Cases"].sum()
    safe1 = az.safest(1)[0]
    risk1 = az.riskiest(1)[0]

    c1, c2, c3, c4 = st.columns(4, gap="small")

    # Static cards
    for col, eye, num, desc in [
        (c1, "Total Records",  f"{total:,}",     "Across all wards · 2020–2024"),
        (c2, "Wards Analysed", f"{len(WARDS)}",  "All 24 BMC municipal wards"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-eye">{eye}</div>
              <div class="kpi-num">{num}</div>
              <div class="kpi-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # Interactive — Safest ward
    with c3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-interactive">
          <div class="kpi-eye">Safest Ward</div>
          <div class="kpi-num">Ward {safe1[0]}</div>
          <div class="kpi-desc">{WARDS[safe1[0]][0]} · {safe1[1]:.0f}/100</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Explore →", key="btn_safest", use_container_width=True):
            st.session_state.selected_ward = safe1[0]
            st.rerun()

    # Interactive — Highest crime ward
    with c4:
        st.markdown(f"""
        <div class="kpi-card kpi-card-interactive">
          <div class="kpi-eye">Highest Crime Ward</div>
          <div class="kpi-num">Ward {risk1[0]}</div>
          <div class="kpi-desc">{WARDS[risk1[0]][0]} · {risk1[1]:.0f}/100</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Explore →", key="btn_riskiest", use_container_width=True):
            st.session_state.selected_ward = risk1[0]
            st.rerun()

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)


def render_ward_detail(info: dict, az: CrimeAnalyzer):
    sc    = info["score"]
    yoy   = int(info["yearly"].get(2024, 0)) - int(info["yearly"].get(2023, 0))
    yoy_s = (f'<span style="color:#991B1B;font-weight:600">+{yoy:,} ↑</span>'
             if yoy > 0 else
             f'<span style="color:#065F46;font-weight:600">{yoy:,} ↓</span>')

    pred_val, pred_ci, slope, _ = predict_2025(info["yearly"])
    chg_pct   = (pred_val - info["yearly"].get(2024, pred_val)) / max(info["yearly"].get(2024, 1), 1) * 100
    chg_str   = f"+{chg_pct:.1f}% vs 2024" if chg_pct >= 0 else f"{chg_pct:.1f}% vs 2024"
    chg_color = "#991B1B" if chg_pct > 0 else "#065F46"
    trend_txt = "Trending up ↑" if slope > 0 else "Trending down ↓"
    zone_short = info["zone"].split("–")[1].strip() if "–" in info["zone"] else info["zone"]
    ci_low  = max(0, int(pred_val - pred_ci))
    ci_high = int(pred_val + pred_ci)

    # Identity + score + stats
    st.markdown(f"""
    <div style="padding:0 2px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
        <div>
          <div style="font-size:10px;font-weight:700;color:#ABABAA;letter-spacing:.10em;text-transform:uppercase">
            Ward {info['ward']}
          </div>
          <div style="font-family:'Sora',sans-serif;font-size:19px;font-weight:700;color:#1A1A18;letter-spacing:-0.03em;margin-top:2px">
            {info['area']}
          </div>
          <div style="font-size:12px;color:#8A8A80;margin-top:2px">{info['zone']}</div>
        </div>
        {_pill(sc)}
      </div>
      <div class="score-wrap">
        <span class="score-num {_score_cls(sc)}">{sc:.0f}</span>
        <span class="score-denom">/ 100</span>
      </div>
      <div style="margin-bottom:16px">
        {_stat("Total cases (2020–24)", f"{info['total']:,}")}
        {_stat("2024 cases", f"{info['yearly'].get(2024,0):,}")}
        {_stat("YoY change (23→24)", yoy_s)}
        {_stat("Zone", zone_short)}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Mini sparkline (trend at a glance)
    st.markdown('<div class="section-lbl">Crime Trend (2020–2024 · ◆ = 2025 est.)</div>',
                unsafe_allow_html=True)
    st.plotly_chart(build_sparkline(info["yearly"]),
                    use_container_width=True,
                    config={"displayModeBar": False})

    # Crime breakdown
    st.markdown('<div class="section-lbl" style="margin-top:14px">Crime Breakdown</div>',
                unsafe_allow_html=True)
    st.markdown(_crime_bars(info["breakdown"]), unsafe_allow_html=True)

    # 2025 Forecast — CI shown as a human-readable range
    st.markdown(f"""
    <div style="margin-top:18px;padding:0 2px">
      <div class="section-lbl">2025 Forecast</div>
      <div class="pred-banner">
        <div>
          <div class="pred-lbl">Predicted Cases</div>
          <div class="pred-val">{pred_val:,.0f}</div>
          <div style="font-size:12px;font-weight:600;color:{chg_color};margin-top:2px">{chg_str}</div>
        </div>
        <div style="text-align:right">
          <div class="pred-lbl">Likely Range</div>
          <div style="font-size:13px;font-weight:600;color:#5A6A7A;margin-top:4px">{ci_low:,} – {ci_high:,}</div>
          <div style="font-size:11px;color:#ABABAA;margin-top:2px">{trend_txt}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🗺</div>
      <div class="empty-title">No Ward Selected</div>
      <div class="empty-sub">
        Pick a ward to see crime stats, trends, and a 2025 forecast.
      </div>
      <div class="empty-ways">
        <span class="empty-way">👆 Click a marker on the map</span>
        <span class="empty-way">🔍 Use the dropdown above</span>
        <span class="empty-way">🏆 Hit "Explore →" on a KPI card</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    st.markdown(CSS, unsafe_allow_html=True)

    df = load_data()
    az = get_analyzer(df)

    if "selected_ward" not in st.session_state:
        st.session_state.selected_ward = None

    render_header(az)
    render_kpis(az)

    # ── SEARCH BAR ──────────────────────────────────────────────
    search_wards = [""] + [f"Ward {w} · {WARDS[w][0]}" for w in WARDS]
    ward_map_inv = {f"Ward {w} · {WARDS[w][0]}": w for w in WARDS}

    # vertical_alignment="bottom" aligns the clear button with the selectbox bottom
    search_col, _, clear_col = st.columns([3, 5, 1], vertical_alignment="bottom")
    with search_col:
        cur_idx = (0 if st.session_state.selected_ward is None
                   else search_wards.index(
                       f"Ward {st.session_state.selected_ward} · "
                       f"{WARDS[st.session_state.selected_ward][0]}"))
        selection = st.selectbox(
            "SEARCH WARD",
            options=search_wards,
            index=cur_idx,
            label_visibility="visible",
            key="ward_search",
        )
        if selection:
            st.session_state.selected_ward = ward_map_inv[selection]

    with clear_col:
        if st.button("✕ Clear", type="secondary", use_container_width=True):
            st.session_state.selected_ward = None
            st.rerun()

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    # ── MAP + DETAIL PANEL ──────────────────────────────────────
    map_col, detail_col = st.columns([57, 43], gap="medium")

    with map_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("""
        <div class="panel-hdr">
          <div class="panel-ttl">Mumbai Ward Safety Map</div>
          <div class="panel-sub">Marker size ∝ crime volume · Color = safety score (green = safe, red = high risk)</div>
        </div>""", unsafe_allow_html=True)

        fig_map = build_map(az, st.session_state.selected_ward)
        event   = st.plotly_chart(
            fig_map, use_container_width=True,
            on_select="rerun", selection_mode=["points"],
            config={"displayModeBar": False},
        )

        # Map affordance hint
        st.markdown("""
        <div class="map-hint">
          <span class="map-hint-dot"></span>
          Click any marker to explore ward details
          <span class="map-hint-dot"></span>
        </div>""", unsafe_allow_html=True)

        # Capture map click
        if event and hasattr(event, "selection") and event.selection:
            pts = event.selection.get("points", [])
            if pts:
                cd = pts[0].get("customdata")
                if cd and len(cd) > 0:
                    clicked = cd[0]
                    if clicked in WARDS and clicked != st.session_state.selected_ward:
                        st.session_state.selected_ward = clicked
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with detail_col:
        st.markdown('<div class="panel"><div class="panel-hdr">', unsafe_allow_html=True)
        ward_title = (
            f"Ward {st.session_state.selected_ward} — {WARDS[st.session_state.selected_ward][0]}"
            if st.session_state.selected_ward else "Ward Detail"
        )
        st.markdown(f"""
          <div class="panel-ttl">{ward_title}</div>
          <div class="panel-sub">{"Crime analysis · 2020–2024 · 2025 forecast"
                                  if st.session_state.selected_ward
                                  else "Select a ward to begin"}</div>
        </div><div class="panel-bod">""", unsafe_allow_html=True)

        if st.session_state.selected_ward:
            info = az.ward_info(st.session_state.selected_ward)
            render_ward_detail(info, az)
        else:
            render_empty_state()

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── BOTTOM TABS ─────────────────────────────────────────────
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏙  City Overview",
        "📈  Trend & 2025 Forecast",
        "🔥  Crime Heatmap",
        "🏆  Safety Rankings",
    ])

    # ── Tab 1: City Overview ────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown('<p class="panel-ttl" style="margin-bottom:12px">Zone-wise Crime Distribution</p>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_zone_bars(az), use_container_width=True,
                            config={"displayModeBar": False})
        with c2:
            st.markdown('<p class="panel-ttl" style="margin-bottom:12px">Crime Type Breakdown (City-wide)</p>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_crime_donut(az), use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        st.markdown('<p class="panel-ttl" style="margin-bottom:12px">Zone-wise Year-over-Year Trend (2020–2024)</p>',
                    unsafe_allow_html=True)
        st.plotly_chart(build_city_trend(az), use_container_width=True,
                        config={"displayModeBar": False})

    # ── Tab 2: Trend & Prediction ───────────────────────────────
    with tab2:
        ward_for_pred = st.session_state.selected_ward

        # Context banner — always visible, adapts to state
        if ward_for_pred:
            area_name = WARDS[ward_for_pred][0]
            st.markdown(f"""
            <div class="tab-banner">
              <span class="tab-banner-ico">📍</span>
              <span class="tab-banner-txt">Ward {ward_for_pred} · {area_name}</span>
              <span class="tab-banner-sub">— ward-specific forecast shown below</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="tab-banner">
              <span class="tab-banner-ico">💡</span>
              <span class="tab-banner-txt">No ward selected</span>
              <span class="tab-banner-sub">— select a ward on the map or dropdown above to see its individual forecast</span>
            </div>""", unsafe_allow_html=True)

        if ward_for_pred:
            info = az.ward_info(ward_for_pred)
            fig_trend, pred_val, pred_ci, slope = build_trend_chart(info)

            p1, p2, p3 = st.columns(3, gap="small")
            trend_dir = "↑ Upward" if slope > 0 else "↓ Downward"
            trend_col = RISK_COLOR if slope > 0 else SAFE_COLOR
            chg24     = pred_val - info["yearly"].get(2024, pred_val)
            ci_low    = max(0, int(pred_val - pred_ci))
            ci_high   = int(pred_val + pred_ci)

            for col, lbl, val, sub in [
                (p1, "2025 Forecast",   f"{pred_val:,.0f} cases",
                                        f"Range: {ci_low:,} – {ci_high:,}"),
                (p2, "Trend Direction", trend_dir,
                                        f"Slope: {slope:+.0f}/yr"),
                (p3, "Change vs 2024",  f"{chg24:+.0f}",
                                        f"{chg24/max(info['yearly'].get(2024,1),1)*100:+.1f}%"),
            ]:
                with col:
                    col_css = f"color:{trend_col}" if lbl == "Trend Direction" else ""
                    st.markdown(f"""
                    <div class="kpi-card">
                      <div class="kpi-eye">{lbl}</div>
                      <div class="kpi-num" style="{col_css}">{val}</div>
                      <div class="kpi-desc">{sub}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
            st.markdown(
                f'<p class="panel-ttl" style="margin-bottom:4px">'
                f'Ward {ward_for_pred} · {WARDS[ward_for_pred][0]} — Crime Trend & 2025 Forecast</p>',
                unsafe_allow_html=True)
            st.markdown(
                '<p style="font-size:12px;color:#ABABAA;margin-bottom:12px">'
                'Blue bars = actual · Terracotta bar = forecast · Dotted line = linear trend</p>',
                unsafe_allow_html=True)
            st.plotly_chart(fig_trend, use_container_width=True,
                            config={"displayModeBar": False})

        # All-wards table — always visible
        st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
        st.markdown('<p class="panel-ttl" style="margin-bottom:12px">All Wards · 2025 Forecast Summary</p>',
                    unsafe_allow_html=True)

        rows_pred = []
        for w in WARDS:
            inf = az.ward_info(w)
            p, ci_w, sl, _ = predict_2025(inf["yearly"])
            act24 = int(inf["yearly"].get(2024, 0))
            chg   = p - act24
            rows_pred.append({
                "Ward": w,
                "Area": WARDS[w][0],
                "Zone": WARDS[w][1].split("–")[1].strip() if "–" in WARDS[w][1] else WARDS[w][1],
                "2024 Actual": act24,
                "2025 Forecast": int(p),
                "Likely Range": f"{max(0,int(p-ci_w)):,} – {int(p+ci_w):,}",
                "Change": int(chg),
                "Change %": round(chg / max(act24, 1) * 100, 1),
                "Safety Score": az.scores[w],
                "Trend": "↑" if sl > 0 else "↓",
            })
        df_pred = (pd.DataFrame(rows_pred)
                   .sort_values("2025 Forecast", ascending=False)
                   .reset_index(drop=True))
        df_pred.index += 1
        st.dataframe(
            df_pred,
            use_container_width=True,
            column_config={
                "Change %": st.column_config.NumberColumn(format="%.1f%%"),
                "Safety Score": st.column_config.ProgressColumn(
                    min_value=0, max_value=100, format="%.0f"),
            },
        )

    # ── Tab 3: Heatmap ──────────────────────────────────────────
    with tab3:
        st.markdown('<p class="panel-ttl" style="margin-bottom:4px">Ward × Crime Type Heatmap</p>',
                    unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#ABABAA;margin-bottom:16px">'
                    'Darker red = higher case count · Scroll vertically if needed</p>',
                    unsafe_allow_html=True)
        st.plotly_chart(build_heatmap(az), use_container_width=True,
                        config={"displayModeBar": False})

    # ── Tab 4: Rankings ─────────────────────────────────────────
    with tab4:
        r1, r2, r3 = st.columns([2, 1, 2], gap="large")

        with r1:
            st.markdown('<p class="panel-ttl" style="margin-bottom:12px">✅ Safest Wards</p>',
                        unsafe_allow_html=True)
            html = ""
            for i, (w, sc) in enumerate(az.safest(10), 1):
                html += _rank_row(i, w, WARDS[w][0], sc)
            st.markdown(html, unsafe_allow_html=True)

        with r2:
            scores_list = list(az.scores.values())
            avg_sc      = sum(scores_list) / len(scores_list)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_sc,
                number={"suffix": "/100", "font": {"size": 22, "family": "Sora", "color": NAVY}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont_size": 9},
                    "bar":  {"color": NAVY, "thickness": 0.22},
                    "bgcolor": "#F7F7F5",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40],   "color": "#FEE2E2"},
                        {"range": [40, 70],  "color": "#FEF3C7"},
                        {"range": [70, 100], "color": "#D1FAE5"},
                    ],
                },
            ))
            fig_g.update_layout(
                paper_bgcolor="white", plot_bgcolor="white",
                height=200, margin=dict(l=20, r=20, t=30, b=0),
                font_family="DM Sans",
            )
            st.markdown('<p class="panel-ttl" style="margin-bottom:4px;text-align:center">City Avg</p>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_g, use_container_width=True,
                            config={"displayModeBar": False})
            st.markdown(f"""
            <div style="text-align:center;margin-top:8px">
              <div style="font-size:11px;color:#ABABAA">Highest: <b style="color:{SAFE_COLOR}">{max(scores_list):.0f}</b></div>
              <div style="font-size:11px;color:#ABABAA;margin-top:4px">Lowest: <b style="color:{RISK_COLOR}">{min(scores_list):.0f}</b></div>
            </div>""", unsafe_allow_html=True)

        with r3:
            st.markdown('<p class="panel-ttl" style="margin-bottom:12px">🔴 Highest Risk Wards</p>',
                        unsafe_allow_html=True)
            html = ""
            for i, (w, sc) in enumerate(az.riskiest(10), 1):
                html += _rank_row(i, w, WARDS[w][0], sc)
            st.markdown(html, unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:40px;padding-top:20px;border-top:1px solid #EBEBEA;
                text-align:center;color:#ABABAA;font-size:11px;">
      Mumbai Crime Area Detector &nbsp;·&nbsp; Data: Mumbai Police Open Data &nbsp;·&nbsp;
      Built with Streamlit · Plotly · pandas · numpy
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()