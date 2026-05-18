import streamlit as st
import math
import pandas as pd
from datetime import datetime
from io import BytesIO
import json

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

/* ── Root theme ── */
:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --border:    #30363d;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --warn:      #f78166;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --mono:      'IBM Plex Mono', monospace;
    --sans:      'IBM Plex Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg);
    color: var(--text);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* ── Main container ── */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1100px;
}

/* ── Page title ── */
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

/* ── Section headers ── */
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

/* ── Result card ── */
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

/* ── Metric tiles ── */
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

/* ── Formula display ── */
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
.formula-box .hi { color: var(--accent); }
.formula-box .hi2 { color: var(--accent2); }

/* ── History table ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 6px; }

/* ── Buttons ── */
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
.stButton > button:hover {
    background: var(--accent);
    color: var(--bg);
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent;
    border: 1px solid var(--accent2);
    color: var(--accent2);
    font-family: var(--mono);
    font-size: 0.82rem;
    border-radius: 5px;
    transition: all 0.15s;
}
.stDownloadButton > button:hover {
    background: var(--accent2);
    color: var(--bg);
}

/* ── Inputs ── */
.stNumberInput input, .stSlider {
    font-family: var(--mono);
}

/* ── Info / warning box ── */
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

/* ── Status badge ── */
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
.badge-ok  { background: rgba(63,185,80,0.15);  color: var(--accent2); border: 1px solid rgba(63,185,80,0.3); }
.badge-mid { background: rgba(255,166,0,0.12);  color: #ffa600; border: 1px solid rgba(255,166,0,0.3); }
.badge-bad { background: rgba(247,129,102,0.12); color: var(--warn); border: 1px solid rgba(247,129,102,0.3); }

/* ── Sidebar nav buttons ── */
div[data-testid="stVerticalBlock"] .stRadio > div { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)


# ─── Core Calculation ───────────────────────────────────────────────────────────
def binomial_pb(A: float, S: int, N: int) -> float | None:
    """
    Pb = Σ(x=N to S-1) [ (S-1)! / (x! * (S-1-X)!) ] * A^x * (1-A)^(S-1-X)

    A = Offered Erlangs per source
    S = Number of sources
    N = Number of servers
    """
    if N >= S:
        return 0.0
    if A <= 0:
        return 0.0
    if A >= 1:
        return 1.0

    total = 0.0
    s1 = S - 1  # S-1
    for x in range(N, S):          # x = N to S-1
        try:
            binom = math.factorial(s1) / (math.factorial(x) * math.factorial(s1 - x))
            term  = binom * (A ** x) * ((1 - A) ** (s1 - x))
            total += term
        except (OverflowError, ZeroDivisionError):
            return None
    return min(total, 1.0)


def grade_of_service(pb: float) -> tuple[str, str]:
    if pb <= 0.01:
        return "Excellent", "badge-ok"
    elif pb <= 0.05:
        return "Acceptable", "badge-mid"
    else:
        return "Poor", "badge-bad"


# ─── PDF Generation (pure Python, no extra deps beyond fpdf2) ──────────────────
def generate_pdf(history: list[dict]) -> bytes:
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(30, 50, 80)
        pdf.cell(0, 10, "Binomial Traffic Calculator — History Report", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(4)

        # Formula reminder
        pdf.set_fill_color(240, 245, 255)
        pdf.set_draw_color(100, 140, 200)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(60, 80, 120)
        pdf.multi_cell(0, 5,
            "Formula: Pb = SUM(x=N to S-1) [ (S-1)! / (x!(S-1-X)!) ] * A^x * (1-A)^(S-1-X)\n"
            "Where: A = Erlangs/source, S = Sources, N = Servers, Pb = Blocking probability",
            border=1, fill=True)
        pdf.ln(6)

        # Table header
        col_w = [28, 18, 18, 18, 32, 30, 42]
        headers = ["Timestamp", "A", "S", "N", "Pb (%)", "GoS", "Notes"]
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(30, 50, 80)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        pdf.ln()

        # Rows
        pdf.set_font("Helvetica", "", 8)
        for idx, row in enumerate(history):
            fill = idx % 2 == 0
            pdf.set_fill_color(248, 250, 255) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 30, 30)
            pb_pct = f"{row['Pb']*100:.4f}%"
            gos, _ = grade_of_service(row['Pb'])
            vals = [
                row.get("Timestamp", "")[:16],
                str(row['A']),
                str(row['S']),
                str(row['N']),
                pb_pct,
                gos,
                row.get("Notes", ""),
            ]
            for i, v in enumerate(vals):
                pdf.cell(col_w[i], 6, v, border=1, fill=fill, align="C" if i != 6 else "L")
            pdf.ln()

        # Footer
        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, "Binomial Traffic Calculator — Teletraffic Engineering Tool", align="C")

        return pdf.output(dest="S").encode("latin-1")

    except ImportError:
        # Fallback: CSV-style plain text as bytes if fpdf2 not available
        lines = ["Binomial Traffic Calculator — History Report",
                 f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "",
                 "Timestamp,A,S,N,Pb,Pb(%),GoS,Notes"]
        for r in history:
            gos, _ = grade_of_service(r['Pb'])
            lines.append(f"{r.get('Timestamp','')},{r['A']},{r['S']},{r['N']},"
                         f"{r['Pb']:.6f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}")
        return "\n".join(lines).encode("utf-8")


# ─── Session State Init ─────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Calculator"


# ─── Sidebar Navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">📡 Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Teletraffic Calculator</div>', unsafe_allow_html=True)

    tab = st.radio(
        "Navigation",
        ["🧮  Calculator", "📊  Results", "🗂️  History"],
        label_visibility="collapsed",
    )
    st.session_state.active_tab = tab.split("  ")[1]

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#8b949e; line-height:1.7; font-family:'IBM Plex Mono',monospace;">
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
        st.markdown(f'<div style="font-size:0.75rem;color:#8b949e;font-family:\'IBM Plex Mono\',monospace;">📋 {len(st.session_state.history)} record(s) saved</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Calculator":

    st.markdown('<div class="app-title">Binomial Traffic Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Finite source blocking probability — Binomial model</div>', unsafe_allow_html=True)

    # Formula box
    st.markdown("""
    <div class="formula-box">
    <span class="hi">Pb</span> = Σ <sub>x=N</sub><sup>S-1</sup>
    &nbsp; <span class="hi2">(S-1)!</span> / [x!(S-1-X)!]
    &nbsp;·&nbsp; <span class="hi">A</span><sup>x</sup>
    &nbsp;·&nbsp; (1-<span class="hi">A</span>)<sup>(S-1-X)</sup>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        A = st.number_input(
            "A — Offered Erlangs per Source",
            min_value=0.001, max_value=0.999,
            value=0.1, step=0.001, format="%.4f",
            help="Traffic intensity offered by each individual source (0 < A < 1)"
        )
    with col2:
        S = st.number_input(
            "S — Number of Sources",
            min_value=2, max_value=500,
            value=10, step=1,
            help="Total number of traffic sources in the group"
        )
    with col3:
        N = st.number_input(
            "N — Number of Servers",
            min_value=1, max_value=499,
            value=3, step=1,
            help="Number of available servers (trunks/circuits)"
        )

    # Validation
    if N >= S:
        st.markdown(f'<div class="warn-box">⚠ N must be less than S. Currently N={N} ≥ S={S}. Pb will be 0 (no blocking possible).</div>', unsafe_allow_html=True)

    # Notes
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
            st.markdown('<div class="warn-box">⚠ Computation failed — values may be too large for factorial calculation. Try reducing S.</div>', unsafe_allow_html=True)
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
            st.success(f"✓ Calculated successfully — {len(st.session_state.history)} total records")

    # Show last result preview inline
    if st.session_state.last_result:
        r = st.session_state.last_result
        gos, badge_cls = grade_of_service(r["Pb"])
        st.markdown('<div class="section-header">Quick Result</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card" style="display:flex; gap:2rem; align-items:center; flex-wrap:wrap;">
            <div>
                <div class="result-big">{r['Pb']*100:.4f}%</div>
                <div class="result-label">Blocking Probability (Pb)</div>
            </div>
            <div style="flex:1;">
                <div class="metric-row">
                    <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A (Erlang/src)</div></div>
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
        st.markdown('<div class="info-box">ℹ No calculation yet. Go to the <b>Calculator</b> tab and run a computation first.</div>', unsafe_allow_html=True)
    else:
        r = st.session_state.last_result
        pb = r["Pb"]
        gos, badge_cls = grade_of_service(pb)
        total_traffic = r['A'] * r['S']
        offered_load  = total_traffic
        carried_load  = total_traffic * (1 - pb)
        blocked_calls  = total_traffic * pb

        # Main result
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
                    <div class="result-sub">As a decimal: <code style="color:#58a6ff;">{pb:.8f}</code></div>
                    <div class="result-sub">Recorded: <code style="font-size:0.8rem;color:#8b949e;">{r['Timestamp']}</code></div>
                    {"<div class='result-sub'><i>" + r['Notes'] + "</i></div>" if r['Notes'] else ""}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Input parameters
        st.markdown('<div class="section-header">Input Parameters</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A — Erlangs/Source</div></div>
            <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S — Sources</div></div>
            <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N — Servers</div></div>
            <div class="metric-tile"><div class="val">{r['S'] - r['N']}</div><div class="lbl">S - N (Excess Src)</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Derived metrics
        st.markdown('<div class="section-header">Derived Traffic Metrics</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{offered_load:.4f}</div><div class="lbl">Total Offered (Erl)</div></div>
            <div class="metric-tile"><div class="val">{carried_load:.4f}</div><div class="lbl">Carried Load (Erl)</div></div>
            <div class="metric-tile"><div class="val">{blocked_calls:.4f}</div><div class="lbl">Blocked Traffic (Erl)</div></div>
            <div class="metric-tile"><div class="val">{(1-pb)*100:.4f}%</div><div class="lbl">Throughput Rate</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Sensitivity hint
        st.markdown('<div class="section-header">Sensitivity Analysis — Add 1 Server</div>', unsafe_allow_html=True)
        pb_plus1 = binomial_pb(r['A'], r['S'], r['N'] + 1)
        if pb_plus1 is not None and r['N'] + 1 < r['S']:
            delta = pb - pb_plus1
            gos2, badge2 = grade_of_service(pb_plus1)
            st.markdown(f"""
            <div class="info-box">
            Adding 1 more server (N → <b>{r['N']+1}</b>) would reduce Pb from
            <b>{pb*100:.4f}%</b> to <b>{pb_plus1*100:.4f}%</b>
            &nbsp;(Δ = −{delta*100:.4f} pp) &nbsp; <span class="badge {badge2}">{gos2}</span>
            </div>
            """, unsafe_allow_html=True)

        # Formula walkthrough
        with st.expander("📐 Formula Walkthrough"):
            st.markdown(f"""
            **Binomial Blocking Formula:**

            ```
            Pb = Σ(x = N to S-1) [ (S-1)! / (x! · (S-1-x)!) ] · A^x · (1-A)^(S-1-x)
            ```

            **With your values** — A = {r['A']}, S = {r['S']}, N = {r['N']}:

            - Summation runs from x = **{r['N']}** to x = **{r['S']-1}**
            - Total terms evaluated: **{r['S'] - r['N']}**
            - S-1 = **{r['S']-1}**, (1-A) = **{1-r['A']:.4f}**

            Each term represents the probability that exactly *x* out of *S-1* sources
            are simultaneously active, weighted by the binomial coefficient.
            The sum gives total probability that all N servers are occupied when a new call arrives.
            """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "History":

    st.markdown('<div class="app-title">Calculation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">All computations in this session</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown('<div class="info-box">ℹ No history yet. Run calculations in the <b>Calculator</b> tab.</div>', unsafe_allow_html=True)
    else:
        n = len(st.session_state.history)

        # Summary stats row
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

        # Build dataframe
        rows = []
        for i, r in enumerate(reversed(st.session_state.history), 1):
            gos, _ = grade_of_service(r["Pb"])
            rows.append({
                "#": n - i + 1,
                "Timestamp": r["Timestamp"],
                "A": r["A"],
                "S": r["S"],
                "N": r["N"],
                "Pb (decimal)": f"{r['Pb']:.8f}",
                "Pb (%)": f"{r['Pb']*100:.4f}%",
                "GoS": gos,
                "Notes": r.get("Notes", ""),
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
        col_dl1, col_dl2, col_clr, _ = st.columns([1.2, 1.2, 1, 3])

        # PDF Download
        with col_dl1:
            pdf_bytes = generate_pdf(st.session_state.history)
            # Determine extension based on content
            ext = "pdf" if pdf_bytes[:4] == b"%PDF" or b"%" in pdf_bytes[:10] else "txt"
            try:
                # Try PDF generation
                from fpdf import FPDF
                pdf_bytes = generate_pdf(st.session_state.history)
                file_ext = "pdf"
                mime_type = "application/pdf"
                btn_label = "⬇  Download PDF"
            except ImportError:
                file_ext = "csv"
                mime_type = "text/plain"
                btn_label = "⬇  Download CSV"

            st.download_button(
                label=btn_label,
                data=pdf_bytes,
                file_name=f"binomial_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                mime=mime_type,
                use_container_width=True,
            )

        # CSV Download
        with col_dl2:
            csv_rows = ["Timestamp,A,S,N,Pb,Pb(%),GoS,Notes"]
            for r in st.session_state.history:
                gos, _ = grade_of_service(r["Pb"])
                csv_rows.append(
                    f"{r['Timestamp']},{r['A']},{r['S']},{r['N']},"
                    f"{r['Pb']:.8f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}"
                )
            csv_data = "\n".join(csv_rows)
            st.download_button(
                label="⬇  Download CSV",
                data=csv_data.encode("utf-8"),
                file_name=f"binomial_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # Clear history
        with col_clr:
            if st.button("🗑  Clear All", use_container_width=True):
                st.session_state.history = []
                st.session_state.last_result = None
                st.rerun()

        st.markdown('<div class="section-header">Blocking Probability Trend</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Record": list(range(1, n + 1)),
            "Pb (%)": [r["Pb"] * 100 for r in st.session_state.history],
        }).set_index("Record")
        st.line_chart(chart_data, height=220)
