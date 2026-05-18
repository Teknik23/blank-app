import streamlit as st
import math
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
from io import BytesIO


# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Binomial Traffic Calculator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

:root {
    --bg:      #0d1117;
    --surface: #161b22;
    --border:  #30363d;
    --accent:  #58a6ff;
    --accent2: #3fb950;
    --warn:    #f78166;
    --text:    #e6edf3;
    --muted:   #8b949e;
    --mono:    'IBM Plex Mono', monospace;
    --sans:    'IBM Plex Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg);
    color: var(--text);
}

section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1200px;
}

.app-title {
    font-family: var(--mono);
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: -0.5px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.6rem;
    margin-bottom: 0.25rem;
}
.app-subtitle {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 2rem;
    font-family: var(--mono);
}

.section-header {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin: 1.8rem 0 1.2rem;
}

.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin: 1rem 0;
}
.result-big {
    font-family: var(--mono);
    font-size: 2.6rem;
    font-weight: 600;
    color: var(--accent2);
    letter-spacing: -1px;
}
.result-label {
    font-size: 0.78rem;
    color: var(--muted);
    font-family: var(--mono);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.result-sub {
    font-size: 0.88rem;
    color: var(--muted);
    margin-top: 0.8rem;
}

.metric-row { display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }
.metric-tile {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    flex: 1;
    min-width: 130px;
}
.metric-tile .val {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
}
.metric-tile .lbl {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}

.formula-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 6px 6px 0;
    padding: 1rem 1.4rem;
    font-family: var(--mono);
    font-size: 0.88rem;
    color: var(--muted);
    margin: 1rem 0;
    line-height: 1.9;
}
.formula-box .hi  { color: var(--accent); }
.formula-box .hi2 { color: var(--accent2); }

.stDataFrame { border: 1px solid var(--border) !important; border-radius: 6px; }

.stButton > button {
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--accent);
    font-family: var(--mono);
    font-size: 0.82rem;
    letter-spacing: 0.5px;
    border-radius: 5px;
    padding: 0.45rem 1.2rem;
    transition: all 0.15s;
}
.stButton > button:hover { background: var(--accent); color: var(--bg); }

.stDownloadButton > button {
    background: transparent;
    border: 1px solid var(--accent2);
    color: var(--accent2);
    font-family: var(--mono);
    font-size: 0.82rem;
    border-radius: 5px;
    transition: all 0.15s;
}
.stDownloadButton > button:hover { background: var(--accent2); color: var(--bg); }

.stNumberInput input { font-family: var(--mono); }

.info-box {
    background: rgba(88,166,255,0.07);
    border: 1px solid rgba(88,166,255,0.3);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.83rem;
    color: var(--muted);
    margin: 0.8rem 0;
}
.warn-box {
    background: rgba(247,129,102,0.07);
    border: 1px solid rgba(247,129,102,0.3);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.83rem;
    color: var(--warn);
    margin: 0.8rem 0;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-ok  { background: rgba(63,185,80,0.15);   color: #3fb950; border: 1px solid rgba(63,185,80,0.3); }
.badge-mid { background: rgba(255,166,0,0.12);   color: #ffa600; border: 1px solid rgba(255,166,0,0.3); }
.badge-bad { background: rgba(247,129,102,0.12); color: #f78166; border: 1px solid rgba(247,129,102,0.3); }

div[data-testid="stVerticalBlock"] .stRadio > div { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def binomial_pb(A: float, S: int, N: int):
    """Pb = Σ(x=N to S-1) C(S-1, x) · A^x · (1-A)^(S-1-x)"""
    if N >= S:  return 0.0
    if A <= 0:  return 0.0
    if A >= 1:  return 1.0
    total = 0.0
    s1 = S - 1
    for x in range(N, S):
        try:
            binom = math.factorial(s1) / (math.factorial(x) * math.factorial(s1 - x))
            total += binom * (A ** x) * ((1 - A) ** (s1 - x))
        except (OverflowError, ZeroDivisionError):
            return None
    return min(total, 1.0)


def grade_of_service(pb: float):
    if pb <= 0.01: return "Excellent", "badge-ok",  "#3fb950"
    if pb <= 0.05: return "Acceptable","badge-mid", "#ffa600"
    return "Poor", "badge-bad", "#f78166"


def _safe(text: str) -> str:
    replacements = {"\u2014":"-","\u2013":"-","\u2018":"'","\u2019":"'",
                    "\u201c":'"',"\u201d":'"',"\u2026":"...","\u00d7":"x"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


# ─── Matplotlib chart helpers ───────────────────────────────────────────────────

_MPL_STYLE = dict(
    facecolor="#161b22", edgecolor="#30363d",
    text_color="#e6edf3", muted="#8b949e",
    accent="#58a6ff", accent2="#3fb950", warn="#f78166",
    grid="#30363d",
)

def _apply_dark(fig, ax):
    s = _MPL_STYLE
    fig.patch.set_facecolor(s["facecolor"])
    ax.set_facecolor(s["facecolor"])
    ax.tick_params(colors=s["muted"], labelsize=8)
    ax.xaxis.label.set_color(s["muted"])
    ax.yaxis.label.set_color(s["muted"])
    ax.title.set_color(s["text_color"])
    for spine in ax.spines.values():
        spine.set_edgecolor(s["grid"])
    ax.grid(color=s["grid"], linestyle="--", linewidth=0.5, alpha=0.7)


def chart_pb_vs_n(A, S, current_N) -> BytesIO:
    """Line chart: Pb as N increases from 1 to S-1."""
    ns = list(range(1, S))
    pbs = [binomial_pb(A, S, n) for n in ns]
    pbs = [p if p is not None else float("nan") for p in pbs]

    fig, ax = plt.subplots(figsize=(7, 3.4))
    _apply_dark(fig, ax)

    ax.plot(ns, [p * 100 for p in pbs], color=_MPL_STYLE["accent"], linewidth=2, zorder=3)
    ax.fill_between(ns, [p * 100 for p in pbs], alpha=0.1, color=_MPL_STYLE["accent"])

    # Horizontal GoS lines
    ax.axhline(1,  color=_MPL_STYLE["accent2"], linestyle=":", linewidth=1, alpha=0.8, label="1% (Excellent)")
    ax.axhline(5,  color="#ffa600",              linestyle=":", linewidth=1, alpha=0.8, label="5% (Acceptable)")

    # Highlight current N
    cur_pb = binomial_pb(A, S, current_N)
    if cur_pb is not None and 1 <= current_N < S:
        ax.axvline(current_N, color=_MPL_STYLE["warn"], linestyle="--", linewidth=1.2, alpha=0.9)
        ax.scatter([current_N], [cur_pb * 100], color=_MPL_STYLE["warn"], s=60, zorder=5)
        ax.annotate(f"N={current_N}\n{cur_pb*100:.3f}%",
                    xy=(current_N, cur_pb * 100),
                    xytext=(12, 8), textcoords="offset points",
                    fontsize=7, color=_MPL_STYLE["warn"],
                    fontfamily="monospace")

    ax.set_xlabel("N — Number of Servers", fontsize=9)
    ax.set_ylabel("Pb (%)", fontsize=9)
    ax.set_title(f"Blocking Probability vs. Servers  (A={A}, S={S})", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, facecolor=_MPL_STYLE["facecolor"],
              edgecolor=_MPL_STYLE["grid"], labelcolor=_MPL_STYLE["muted"])
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_pb_vs_a(S, N) -> BytesIO:
    """Line chart: Pb as A varies 0.01 → 0.99."""
    As = [round(a * 0.01, 2) for a in range(1, 100)]
    pbs = [binomial_pb(a, S, N) for a in As]
    pbs = [p if p is not None else float("nan") for p in pbs]

    fig, ax = plt.subplots(figsize=(7, 3.4))
    _apply_dark(fig, ax)

    ax.plot(As, [p * 100 for p in pbs], color=_MPL_STYLE["accent2"], linewidth=2)
    ax.fill_between(As, [p * 100 for p in pbs], alpha=0.1, color=_MPL_STYLE["accent2"])
    ax.axhline(1, color=_MPL_STYLE["accent2"], linestyle=":", linewidth=1, alpha=0.7, label="1%")
    ax.axhline(5, color="#ffa600",             linestyle=":", linewidth=1, alpha=0.7, label="5%")

    ax.set_xlabel("A — Erlangs / Source", fontsize=9)
    ax.set_ylabel("Pb (%)", fontsize=9)
    ax.set_title(f"Blocking Probability vs. Traffic Intensity  (S={S}, N={N})", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, facecolor=_MPL_STYLE["facecolor"],
              edgecolor=_MPL_STYLE["grid"], labelcolor=_MPL_STYLE["muted"])
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_gos_distribution(history: list) -> BytesIO:
    """Pie / donut chart of GoS categories in history."""
    counts = {"Excellent": 0, "Acceptable": 0, "Poor": 0}
    for r in history:
        gos, _, _ = grade_of_service(r["Pb"])
        counts[gos] += 1

    labels = [k for k, v in counts.items() if v > 0]
    sizes  = [v for v in counts.values() if v > 0]
    colors = [_MPL_STYLE["accent2"] if l == "Excellent"
              else "#ffa600" if l == "Acceptable"
              else _MPL_STYLE["warn"]
              for l in labels]

    fig, ax = plt.subplots(figsize=(4.5, 3.4))
    _apply_dark(fig, ax)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, wedgeprops=dict(linewidth=0.5, edgecolor=_MPL_STYLE["facecolor"]),
        pctdistance=0.75,
    )
    for t in texts:    t.set_color(_MPL_STYLE["muted"]); t.set_fontsize(8)
    for t in autotexts: t.set_color(_MPL_STYLE["facecolor"]); t.set_fontsize(8); t.set_fontweight("bold")

    # Draw centre hole (donut)
    circle = plt.Circle((0, 0), 0.50, color=_MPL_STYLE["facecolor"])
    ax.add_artist(circle)
    ax.set_title("Grade of Service Distribution", fontsize=10, fontweight="bold",
                 color=_MPL_STYLE["text_color"])
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_pb_trend(history: list) -> BytesIO:
    """Pb trend line across all history records."""
    xs  = list(range(1, len(history) + 1))
    pbs = [r["Pb"] * 100 for r in history]

    fig, ax = plt.subplots(figsize=(7, 3))
    _apply_dark(fig, ax)

    ax.plot(xs, pbs, color=_MPL_STYLE["accent"], linewidth=2, marker="o",
            markersize=5, markerfacecolor=_MPL_STYLE["accent2"], markeredgewidth=0)
    ax.fill_between(xs, pbs, alpha=0.08, color=_MPL_STYLE["accent"])
    ax.axhline(1, color=_MPL_STYLE["accent2"], linestyle=":", linewidth=1, alpha=0.7, label="1% GoS")
    ax.axhline(5, color="#ffa600",             linestyle=":", linewidth=1, alpha=0.7, label="5% GoS")

    ax.set_xlabel("Record #", fontsize=9)
    ax.set_ylabel("Pb (%)", fontsize=9)
    ax.set_title("Blocking Probability — Session Trend", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, facecolor=_MPL_STYLE["facecolor"],
              edgecolor=_MPL_STYLE["grid"], labelcolor=_MPL_STYLE["muted"])
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_heatmap(A, S_max=30) -> BytesIO:
    """Heatmap: Pb for varying N and S (fixed A)."""
    S_vals = list(range(2, min(S_max + 1, 31)))
    N_vals = list(range(1, min(S_max, 30)))
    data = []
    for s in S_vals:
        row = []
        for n in N_vals:
            if n < s:
                pb = binomial_pb(A, s, n)
                row.append(pb * 100 if pb is not None else float("nan"))
            else:
                row.append(float("nan"))
        data.append(row)

    arr = np.array(data)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    _apply_dark(fig, ax)
    im = ax.imshow(arr, aspect="auto", cmap="RdYlGn_r",
                   vmin=0, vmax=min(np.nanmax(arr), 30),
                   origin="lower", extent=[0.5, len(N_vals) + 0.5, 1.5, len(S_vals) + 0.5])

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.ax.tick_params(colors=_MPL_STYLE["muted"], labelsize=7)
    cbar.set_label("Pb (%)", color=_MPL_STYLE["muted"], fontsize=8)

    ax.set_xticks(range(1, len(N_vals) + 1))
    ax.set_xticklabels(N_vals, fontsize=6)
    ax.set_yticks(range(2, len(S_vals) + 2))
    ax.set_yticklabels(S_vals, fontsize=6)
    ax.set_xlabel("N — Servers", fontsize=9)
    ax.set_ylabel("S — Sources", fontsize=9)
    ax.set_title(f"Pb Heatmap (%) — A = {A}", fontsize=10, fontweight="bold")
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


# ─── PDF Generation ─────────────────────────────────────────────────────────────

def generate_pdf(history: list, chart_bufs: dict = None) -> bytes:
    """Generate PDF report with history table and optional embedded charts."""
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=18)

        # ── PAGE 1: Cover + Summary ──────────────────────────────────────────
        pdf.add_page()

        # Header bar
        pdf.set_fill_color(13, 17, 23)
        pdf.rect(0, 0, 210, 28, "F")
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_text_color(88, 166, 255)
        pdf.set_xy(10, 8)
        pdf.cell(0, 8, _safe("Binomial Traffic Calculator"), ln=False)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(139, 148, 158)
        pdf.set_xy(10, 18)
        pdf.cell(0, 5, _safe(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
        pdf.ln(6)

        # Formula box
        pdf.set_fill_color(240, 245, 255)
        pdf.set_draw_color(88, 140, 200)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(60, 80, 120)
        pdf.multi_cell(0, 5,
            _safe("Formula: Pb = SUM(x=N to S-1) [ (S-1)! / (x! (S-1-x)!) ] * A^x * (1-A)^(S-1-x)\n"
                  "A = Erlangs/source  |  S = Sources  |  N = Servers  |  Pb = Blocking Probability"),
            border=1, fill=True)
        pdf.ln(5)

        # Summary stats
        pbs = [r["Pb"] for r in history]
        n   = len(history)
        stats = [
            ("Total Records",   str(n)),
            ("Min Pb",          f"{min(pbs)*100:.4f}%"),
            ("Max Pb",          f"{max(pbs)*100:.4f}%"),
            ("Avg Pb",          f"{sum(pbs)/n*100:.4f}%"),
        ]
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 50, 80)
        pdf.cell(0, 6, _safe("Session Summary"), ln=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(50, 50, 50)
        tile_w = 44
        for i, (lbl, val) in enumerate(stats):
            x = 10 + i * (tile_w + 4)
            pdf.set_xy(x, pdf.get_y())
            pdf.set_fill_color(245, 248, 255)
            pdf.set_draw_color(200, 210, 230)
            pdf.rect(x, pdf.get_y(), tile_w, 16, "DF")
            pdf.set_xy(x + 2, pdf.get_y() + 2)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(30, 50, 80)
            pdf.cell(tile_w - 4, 5, _safe(val), ln=False)
            pdf.set_xy(x + 2, pdf.get_y() + 5)
            pdf.set_font("Helvetica", "", 6.5)
            pdf.set_text_color(120, 130, 150)
            pdf.cell(tile_w - 4, 4, _safe(lbl), ln=False)
        pdf.ln(22)

        # ── Embed charts ────────────────────────────────────────────────────
        if chart_bufs:
            chart_items = list(chart_bufs.items())

            # Two charts side by side per row
            for i in range(0, len(chart_items), 2):
                row_items = chart_items[i:i+2]
                y_start = pdf.get_y()
                chart_h = 62
                chart_w = 90

                for j, (title, buf) in enumerate(row_items):
                    x = 10 + j * (chart_w + 10)
                    buf.seek(0)

                    # Save to temp file
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                        tmp.write(buf.read())
                        tmp_path = tmp.name

                    # Chart title
                    pdf.set_xy(x, y_start)
                    pdf.set_font("Helvetica", "B", 7)
                    pdf.set_text_color(60, 80, 120)
                    pdf.cell(chart_w, 5, _safe(title), ln=False, align="C")

                    # Image
                    pdf.image(tmp_path, x=x, y=y_start + 5, w=chart_w, h=chart_h)
                    os.unlink(tmp_path)

                pdf.ln(chart_h + 12)

        # ── PAGE 2: Data Table ───────────────────────────────────────────────
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 50, 80)
        pdf.cell(0, 8, _safe("Calculation History"), ln=True)
        pdf.ln(2)

        col_w = [28, 16, 14, 14, 30, 26, 22, 40]
        headers = ["Timestamp", "A", "S", "N", "Pb (decimal)", "Pb (%)", "GoS", "Notes"]
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(30, 50, 80)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 7, _safe(h), border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 7.5)
        for idx, row in enumerate(history):
            fill = idx % 2 == 0
            pdf.set_fill_color(248, 250, 255) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 30, 30)
            gos, _, _ = grade_of_service(row["Pb"])
            vals = [
                row.get("Timestamp", "")[:16],
                str(row["A"]),
                str(row["S"]),
                str(row["N"]),
                f"{row['Pb']:.8f}",
                f"{row['Pb']*100:.4f}%",
                gos,
                row.get("Notes", ""),
            ]
            aligns = ["C","C","C","C","C","C","C","L"]
            for i, v in enumerate(vals):
                pdf.cell(col_w[i], 6, _safe(v), border=1, fill=fill, align=aligns[i])
            pdf.ln()

        # Footer
        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, _safe("Binomial Traffic Calculator — Teletraffic Engineering Tool"), align="C")

        result = pdf.output()
        return bytes(result) if isinstance(result, (bytes, bytearray)) else result.encode("latin-1")

    except ImportError:
        lines = ["Binomial Traffic Calculator - History Report",
                 f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "",
                 "Timestamp,A,S,N,Pb,Pb(%),GoS,Notes"]
        for r in history:
            gos, _, _ = grade_of_service(r["Pb"])
            lines.append(f"{r.get('Timestamp','')},{r['A']},{r['S']},{r['N']},"
                         f"{r['Pb']:.6f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}")
        return "\n".join(lines).encode("utf-8")


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
if "history"     not in st.session_state: st.session_state.history     = []
if "last_result" not in st.session_state: st.session_state.last_result = None
if "active_tab"  not in st.session_state: st.session_state.active_tab  = "Calculator"


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="app-title">📡 Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Teletraffic Calculator</div>', unsafe_allow_html=True)

    tab = st.radio(
        "Navigation",
        ["🧮  Calculator", "📊  Results", "📈  Analysis", "🗂️  History"],
        label_visibility="collapsed",
    )
    st.session_state.active_tab = tab.split("  ")[1]

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#8b949e; line-height:1.9; font-family:'IBM Plex Mono',monospace;">
    <b style="color:#58a6ff;">VARIABLES</b><br>
    <b>A</b> — Erlangs / source<br>
    <b>S</b> — Total sources<br>
    <b>N</b> — Servers (circuits)<br>
    <b>Pb</b> — Blocking prob.<br><br>
    <b style="color:#58a6ff;">FORMULA</b><br>
    Engset-class finite<br>
    source model with<br>
    retrial assumption.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        n_rec = len(st.session_state.history)
        st.markdown(
            f'<div style="font-size:0.75rem;color:#8b949e;font-family:\'IBM Plex Mono\',monospace;">'
            f'📋 {n_rec} record(s) saved</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Calculator":

    st.markdown('<div class="app-title">Binomial Traffic Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Finite source blocking probability — Binomial model</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    <span class="hi">Pb</span> = &Sigma;<sub>x=N</sub><sup>S-1</sup>
    &nbsp;<span class="hi2">(S-1)!</span> / [x! &middot; (S-1-x)!]
    &nbsp;&middot;&nbsp; <span class="hi">A</span><sup>x</sup>
    &nbsp;&middot;&nbsp; (1&minus;<span class="hi">A</span>)<sup>(S-1-x)</sup>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        A = st.number_input("A — Offered Erlangs per Source",
                            min_value=0.001, max_value=0.999,
                            value=0.1, step=0.001, format="%.4f",
                            help="Traffic intensity offered by each individual source (0 < A < 1)")
    with col2:
        S = st.number_input("S — Number of Sources",
                            min_value=2, max_value=500,
                            value=10, step=1,
                            help="Total number of traffic sources in the group")
    with col3:
        N = st.number_input("N — Number of Servers",
                            min_value=1, max_value=499,
                            value=3, step=1,
                            help="Number of available servers (trunks/circuits)")

    if N >= S:
        st.markdown(
            f'<div class="warn-box">⚠ N must be less than S. '
            f'Currently N={N} ≥ S={S}. Pb will be 0 (no blocking possible).</div>',
            unsafe_allow_html=True,
        )

    notes = st.text_input("Notes (optional)", placeholder="e.g. Scenario A — peak hour traffic", max_chars=80)

    st.markdown('<div class="section-header">Action</div>', unsafe_allow_html=True)

    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    with col_btn1:
        calc_btn = st.button("▶  Calculate", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("✕  Clear", use_container_width=True)

    if clear_btn:
        st.session_state.last_result = None
        st.rerun()

    if calc_btn:
        with st.spinner("Computing..."):
            pb = binomial_pb(float(A), int(S), int(N))

        if pb is None:
            st.markdown(
                '<div class="warn-box">⚠ Computation failed — values may be too large. Try reducing S.</div>',
                unsafe_allow_html=True,
            )
        else:
            result = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "A": round(float(A), 4),
                "S": int(S),
                "N": int(N),
                "Pb": pb,
                "Notes": notes,
            }
            st.session_state.last_result = result
            st.session_state.history.append(result)
            st.success(f"✓ Calculated — {len(st.session_state.history)} total records")

    if st.session_state.last_result:
        r = st.session_state.last_result
        gos, badge_cls, _ = grade_of_service(r["Pb"])
        st.markdown('<div class="section-header">Quick Result</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card" style="display:flex; gap:2rem; align-items:center; flex-wrap:wrap;">
            <div>
                <div class="result-big">{r['Pb']*100:.4f}%</div>
                <div class="result-label">Blocking Probability (Pb)</div>
            </div>
            <div style="flex:1;">
                <div class="metric-row">
                    <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A (Erl/src)</div></div>
                    <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S (Sources)</div></div>
                    <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N (Servers)</div></div>
                    <div class="metric-tile"><div class="val"><span class="badge {badge_cls}">{gos}</span></div><div class="lbl">Grade of Service</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Results":

    st.markdown('<div class="app-title">Calculation Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Detailed breakdown of the latest computation</div>', unsafe_allow_html=True)

    if not st.session_state.last_result:
        st.markdown('<div class="info-box">ℹ No calculation yet. Go to the <b>Calculator</b> tab first.</div>', unsafe_allow_html=True)
    else:
        r   = st.session_state.last_result
        pb  = r["Pb"]
        gos, badge_cls, _ = grade_of_service(pb)
        total_traffic = r["A"] * r["S"]
        carried_load  = total_traffic * (1 - pb)
        blocked_calls = total_traffic * pb

        st.markdown('<div class="section-header">Primary Result</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex; align-items:flex-start; gap:2.5rem; flex-wrap:wrap;">
                <div>
                    <div class="result-big">{pb*100:.6f}%</div>
                    <div class="result-label">Blocking Probability (Pb)</div>
                    <div style="margin-top:0.6rem;">
                        <span class="badge {badge_cls}">{gos}</span>
                        &nbsp;<span style="font-size:0.78rem;color:#8b949e;font-family:'IBM Plex Mono',monospace;">Grade of Service</span>
                    </div>
                    <div class="result-sub">Decimal: <code style="color:#58a6ff;">{pb:.8f}</code></div>
                    <div class="result-sub">Recorded: <code style="font-size:0.8rem;color:#8b949e;">{r['Timestamp']}</code></div>
                    {"<div class='result-sub'><i>" + r['Notes'] + "</i></div>" if r['Notes'] else ""}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Input Parameters</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A — Erlangs/Source</div></div>
            <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S — Sources</div></div>
            <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N — Servers</div></div>
            <div class="metric-tile"><div class="val">{r['S'] - r['N']}</div><div class="lbl">S − N (Excess)</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Derived Traffic Metrics</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{total_traffic:.4f}</div><div class="lbl">Offered Load (Erl)</div></div>
            <div class="metric-tile"><div class="val">{carried_load:.4f}</div><div class="lbl">Carried Load (Erl)</div></div>
            <div class="metric-tile"><div class="val">{blocked_calls:.4f}</div><div class="lbl">Blocked Traffic (Erl)</div></div>
            <div class="metric-tile"><div class="val">{(1-pb)*100:.4f}%</div><div class="lbl">Throughput Rate</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Sensitivity — Add 1 Server</div>', unsafe_allow_html=True)
        pb_plus1 = binomial_pb(r["A"], r["S"], r["N"] + 1)
        if pb_plus1 is not None and r["N"] + 1 < r["S"]:
            delta = pb - pb_plus1
            gos2, badge2, _ = grade_of_service(pb_plus1)
            st.markdown(f"""
            <div class="info-box">
            Adding 1 more server (N → <b>{r['N']+1}</b>) would reduce Pb from
            <b>{pb*100:.4f}%</b> to <b>{pb_plus1*100:.4f}%</b>
            &nbsp;(Δ = −{delta*100:.4f} pp) &nbsp;<span class="badge {badge2}">{gos2}</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📐 Formula Walkthrough"):
            st.markdown(f"""
**Binomial Blocking Formula:**
```
Pb = Σ(x = N to S-1)  [ (S-1)! / (x! · (S-1-x)!) ]  ·  A^x  ·  (1-A)^(S-1-x)
```
**With your values** — A = {r['A']}, S = {r['S']}, N = {r['N']}:
- Summation runs from x = **{r['N']}** to x = **{r['S']-1}**
- Total terms evaluated: **{r['S'] - r['N']}**
- S-1 = **{r['S']-1}**,   (1-A) = **{1-r['A']:.4f}**

Each term represents the probability that exactly *x* of *S-1* sources are
simultaneously active. The sum gives the total probability that all N servers
are occupied when a new call arrives.
""")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANALYSIS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Analysis":

    st.markdown('<div class="app-title">Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Interactive charts and sensitivity analysis</div>', unsafe_allow_html=True)

    if not st.session_state.last_result:
        st.markdown('<div class="info-box">ℹ Run at least one calculation in the <b>Calculator</b> tab to unlock charts.</div>', unsafe_allow_html=True)
    else:
        r = st.session_state.last_result
        A_val, S_val, N_val = r["A"], r["S"], r["N"]

        # ── Row 1: Pb vs N  |  Pb vs A ──────────────────────────────────────
        st.markdown('<div class="section-header">Sensitivity — Servers & Traffic Intensity</div>', unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("**Pb vs. Number of Servers (N)**")
            buf1 = chart_pb_vs_n(A_val, S_val, N_val)
            st.image(buf1, use_container_width=True)

        with col_r:
            st.markdown("**Pb vs. Traffic Intensity (A)**")
            buf2 = chart_pb_vs_a(S_val, N_val)
            st.image(buf2, use_container_width=True)

        # ── Row 2: Heatmap ───────────────────────────────────────────────────
        st.markdown('<div class="section-header">Pb Heatmap — N vs S (fixed A)</div>', unsafe_allow_html=True)
        s_max_heat = st.slider("Max S for heatmap", min_value=5, max_value=40, value=min(S_val + 5, 30), step=5)
        buf3 = chart_heatmap(A_val, S_max=s_max_heat)
        st.image(buf3, use_container_width=True)
        st.markdown(
            '<div class="info-box">🟢 Green = low blocking (Excellent) &nbsp;|&nbsp; '
            '🔴 Red = high blocking (Poor) &nbsp;|&nbsp; Grey = N ≥ S (no blocking)</div>',
            unsafe_allow_html=True,
        )

        # ── Row 3: History charts (only if ≥ 2 records) ─────────────────────
        if len(st.session_state.history) >= 2:
            st.markdown('<div class="section-header">Session History Charts</div>', unsafe_allow_html=True)
            col_tl, col_pie = st.columns([2, 1])

            with col_tl:
                st.markdown("**Pb Trend across Records**")
                buf4 = chart_pb_trend(st.session_state.history)
                st.image(buf4, use_container_width=True)

            with col_pie:
                st.markdown("**Grade of Service Distribution**")
                buf5 = chart_gos_distribution(st.session_state.history)
                st.image(buf5, use_container_width=True)

        # ── Sensitivity sweep table ──────────────────────────────────────────
        st.markdown('<div class="section-header">Sensitivity Sweep — N from 1 to S-1</div>', unsafe_allow_html=True)
        sweep_rows = []
        for n_test in range(1, S_val):
            pb_t = binomial_pb(A_val, S_val, n_test)
            if pb_t is not None:
                gos_t, _, _ = grade_of_service(pb_t)
                sweep_rows.append({
                    "N": n_test,
                    "Pb (decimal)": f"{pb_t:.8f}",
                    "Pb (%)": f"{pb_t*100:.4f}%",
                    "GoS": gos_t,
                    "Δ from current": f"{(pb_t - r['Pb'])*100:+.4f} pp",
                })

        sweep_df = pd.DataFrame(sweep_rows)
        st.dataframe(
            sweep_df.style.apply(
                lambda col: [
                    "background-color: rgba(63,185,80,0.08);"  if "Excellent" in str(v)
                    else "background-color: rgba(255,166,0,0.08);" if "Acceptable" in str(v)
                    else "background-color: rgba(247,129,102,0.08);" if "Poor" in str(v)
                    else ""
                    for v in col
                ],
                subset=["GoS"],
            ),
            use_container_width=True,
            hide_index=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "History":

    st.markdown('<div class="app-title">Calculation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">All computations in this session</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown('<div class="info-box">ℹ No history yet. Run calculations in the <b>Calculator</b> tab.</div>', unsafe_allow_html=True)
    else:
        n   = len(st.session_state.history)
        pbs = [r["Pb"] for r in st.session_state.history]

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{n}</div><div class="lbl">Total Records</div></div>
            <div class="metric-tile"><div class="val">{min(pbs)*100:.4f}%</div><div class="lbl">Min Pb</div></div>
            <div class="metric-tile"><div class="val">{max(pbs)*100:.4f}%</div><div class="lbl">Max Pb</div></div>
            <div class="metric-tile"><div class="val">{sum(pbs)/n*100:.4f}%</div><div class="lbl">Avg Pb</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Records</div>', unsafe_allow_html=True)

        rows = []
        for i, row in enumerate(reversed(st.session_state.history), 1):
            gos, _, _ = grade_of_service(row["Pb"])
            rows.append({
                "#": n - i + 1,
                "Timestamp": row["Timestamp"],
                "A": row["A"],
                "S": row["S"],
                "N": row["N"],
                "Pb (decimal)": f"{row['Pb']:.8f}",
                "Pb (%)": f"{row['Pb']*100:.4f}%",
                "GoS": gos,
                "Notes": row.get("Notes", ""),
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Trend chart ──────────────────────────────────────────────────────
        if n >= 2:
            st.markdown('<div class="section-header">Blocking Probability Trend</div>', unsafe_allow_html=True)
            buf_trend = chart_pb_trend(st.session_state.history)
            st.image(buf_trend, use_container_width=True)

        # ── Export ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
        col_dl1, col_dl2, col_clr, _ = st.columns([1.4, 1.4, 1, 2.2])

        with col_dl1:
            # Build charts for PDF
            chart_bufs_pdf = {}
            if st.session_state.last_result:
                r = st.session_state.last_result
                chart_bufs_pdf["Pb vs Servers (N)"]     = chart_pb_vs_n(r["A"], r["S"], r["N"])
                chart_bufs_pdf["Pb vs Traffic (A)"]     = chart_pb_vs_a(r["S"], r["N"])
                chart_bufs_pdf["Pb Heatmap"]            = chart_heatmap(r["A"])
            if n >= 2:
                chart_bufs_pdf["Pb Trend"]              = chart_pb_trend(st.session_state.history)
                chart_bufs_pdf["GoS Distribution"]      = chart_gos_distribution(st.session_state.history)

            try:
                from fpdf import FPDF  # noqa
                pdf_bytes  = generate_pdf(st.session_state.history, chart_bufs=chart_bufs_pdf)
                file_ext   = "pdf"
                mime_type  = "application/pdf"
                btn_label  = "⬇  Download PDF (with Charts)"
            except ImportError:
                pdf_bytes  = generate_pdf(st.session_state.history)
                file_ext   = "txt"
                mime_type  = "text/plain"
                btn_label  = "⬇  Download TXT"

            st.download_button(
                label=btn_label,
                data=pdf_bytes,
                file_name=f"binomial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                mime=mime_type,
                use_container_width=True,
            )

        with col_dl2:
            csv_rows = ["Timestamp,A,S,N,Pb,Pb(%),GoS,Notes"]
            for row in st.session_state.history:
                gos, _, _ = grade_of_service(row["Pb"])
                csv_rows.append(
                    f"{row['Timestamp']},{row['A']},{row['S']},{row['N']},"
                    f"{row['Pb']:.8f},{row['Pb']*100:.4f}%,{gos},{row.get('Notes','')}"
                )
            st.download_button(
                label="⬇  Download CSV",
                data="\n".join(csv_rows).encode("utf-8"),
                file_name=f"binomial_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col_clr:
            if st.button("🗑  Clear All", use_container_width=True):
                st.session_state.history     = []
                st.session_state.last_result = None
                st.rerun()
