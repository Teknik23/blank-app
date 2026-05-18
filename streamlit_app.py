import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

# ─── Konfigurasi Halaman ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator Trafik Binomial",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

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

section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1100px;
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
.stButton > button:hover {
    background: var(--accent);
    color: var(--bg);
}

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

.stNumberInput input, .stSlider {
    font-family: var(--mono);
}

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
.badge-ok  { background: rgba(63,185,80,0.15);  color: var(--accent2); border: 1px solid rgba(63,185,80,0.3); }
.badge-mid { background: rgba(255,166,0,0.12);  color: #ffa600;        border: 1px solid rgba(255,166,0,0.3); }
.badge-bad { background: rgba(247,129,102,0.12); color: var(--warn);   border: 1px solid rgba(247,129,102,0.3); }

div[data-testid="stVerticalBlock"] .stRadio > div { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)


# ─── Fungsi Perhitungan Utama ───────────────────────────────────────────────────
def binomial_pb(A: float, S: int, N: int):
    """
    Pb = Σ(x=N to S-1) [ (S-1)! / (x! * (S-1-x)!) ] * A^x * (1-A)^(S-1-x)
    A = Erlangs per sumber
    S = Jumlah sumber
    N = Jumlah server
    """
    if N >= S:
        return 0.0
    if A <= 0:
        return 0.0
    if A >= 1:
        return 1.0

    total = 0.0
    s1 = S - 1
    for x in range(N, S):
        try:
            binom = math.factorial(s1) / (math.factorial(x) * math.factorial(s1 - x))
            term  = binom * (A ** x) * ((1 - A) ** (s1 - x))
            total += term
        except (OverflowError, ZeroDivisionError):
            return None
    return min(total, 1.0)


def grade_of_service(pb: float):
    if pb <= 0.01:
        return "Sangat Baik", "badge-ok"
    elif pb <= 0.05:
        return "Dapat Diterima", "badge-mid"
    else:
        return "Buruk", "badge-bad"


def _safe(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00d7": "x",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf(history: list) -> bytes:
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(30, 50, 80)
        pdf.cell(0, 10, _safe("Kalkulator Trafik Binomial - Laporan Riwayat"), ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 6, _safe(f"Dibuat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
        pdf.ln(4)

        pdf.set_fill_color(240, 245, 255)
        pdf.set_draw_color(100, 140, 200)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(60, 80, 120)
        pdf.multi_cell(0, 5,
            _safe("Rumus: Pb = JUMLAH(x=N to S-1) [ (S-1)! / (x!(S-1-x)!) ] * A^x * (1-A)^(S-1-x)\n"
                  "Keterangan: A = Erlang/sumber, S = Sumber, N = Server, Pb = Probabilitas blokir"),
            border=1, fill=True)
        pdf.ln(6)

        col_w = [28, 18, 18, 18, 32, 30, 42]
        headers = ["Waktu", "A", "S", "N", "Pb (%)", "GoS", "Catatan"]
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(30, 50, 80)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 7, _safe(h), border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        for idx, row in enumerate(history):
            fill = idx % 2 == 0
            if fill:
                pdf.set_fill_color(248, 250, 255)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 30, 30)
            pb_pct = f"{row['Pb']*100:.4f}%"
            gos, _ = grade_of_service(row['Pb'])
            vals = [
                row.get("Timestamp", "")[:16],
                str(row['A']), str(row['S']), str(row['N']),
                pb_pct, gos, row.get("Notes", ""),
            ]
            for i, v in enumerate(vals):
                pdf.cell(col_w[i], 6, _safe(v), border=1, fill=fill,
                         align="C" if i != 6 else "L")
            pdf.ln()

        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, _safe("Kalkulator Trafik Binomial — Alat Rekayasa Teletrafik"), align="C")

        result = pdf.output()
        if isinstance(result, (bytes, bytearray)):
            return bytes(result)
        return result.encode("latin-1")

    except ImportError:
        lines = [
            "Kalkulator Trafik Binomial - Laporan Riwayat",
            f"Dibuat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "",
            "Waktu,A,S,N,Pb,Pb(%),GoS,Catatan",
        ]
        for r in history:
            gos, _ = grade_of_service(r['Pb'])
            lines.append(
                f"{r.get('Timestamp','')},{r['A']},{r['S']},{r['N']},"
                f"{r['Pb']:.6f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}"
            )
        return "\n".join(lines).encode("utf-8")


# ─── Inisialisasi Status Sesi ───────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Kalkulator"


# ─── Navigasi Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">📡 Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Kalkulator Teletrafik</div>', unsafe_allow_html=True)

    tab_options = ["🧮  Kalkulator", "📊  Hasil", "🗂️  Riwayat"]
    tab = st.radio(
        "Navigasi",
        tab_options,
        label_visibility="collapsed",
    )
    # Ambil nama tab dari pilihan
    active_tab = tab.split("  ", 1)[1] if "  " in tab else tab
    st.session_state.active_tab = active_tab

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#8b949e; line-height:1.9; font-family:'IBM Plex Mono',monospace;">
    <b style="color:#58a6ff;">VARIABEL</b><br>
    <b>A</b> — Erlang / sumber<br>
    <b>S</b> — Total sumber<br>
    <b>N</b> — Server (sirkuit)<br>
    <b>Pb</b> — Probabilitas blokir<br><br>
    <b style="color:#58a6ff;">FORMULA</b><br>
    Model sumber terbatas<br>
    kelas Engset dengan<br>
    asumsi percobaan ulang.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        n_rec = len(st.session_state.history)
        st.markdown(
            f'<div style="font-size:0.75rem;color:#8b949e;font-family:\'IBM Plex Mono\',monospace;">'
            f'📋 {n_rec} data tersimpan</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KALKULATOR
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Kalkulator":

    st.markdown('<div class="app-title">Kalkulator Trafik Binomial</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Probabilitas blokir sumber terbatas — Model Binomial</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="formula-box">
    <span class="hi">Pb</span> = Σ <sub>x=N</sub><sup>S-1</sup>
    &nbsp; <span class="hi2">(S-1)!</span> / [x!(S-1-x)!]
    &nbsp;·&nbsp; <span class="hi">A</span><sup>x</sup>
    &nbsp;·&nbsp; (1-<span class="hi">A</span>)<sup>(S-1-x)</sup>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Parameter Masukan</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        A = st.number_input(
            "A — Erlang yang Ditawarkan per Sumber",
            min_value=0.001, max_value=0.999,
            value=0.1, step=0.001, format="%.4f",
            help="Intensitas trafik yang ditawarkan setiap sumber (0 < A < 1)"
        )
    with col2:
        S = st.number_input(
            "S — Jumlah Sumber",
            min_value=2, max_value=500,
            value=10, step=1,
            help="Total jumlah sumber trafik dalam kelompok"
        )
    with col3:
        N = st.number_input(
            "N — Jumlah Server",
            min_value=1, max_value=499,
            value=3, step=1,
            help="Jumlah server yang tersedia (trunk/sirkuit)"
        )

    if N >= S:
        st.markdown(
            f'<div class="warn-box">⚠ N harus lebih kecil dari S. '
            f'Saat ini N={N} ≥ S={S}. Nilai Pb akan menjadi 0 (tidak ada pemblokiran).</div>',
            unsafe_allow_html=True
        )

    notes = st.text_input(
        "Catatan (opsional)",
        placeholder="contoh: Skenario A — trafik jam sibuk",
        max_chars=80
    )

    st.markdown('<div class="section-header">Aksi</div>', unsafe_allow_html=True)

    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    with col_btn1:
        calc_btn = st.button("▶  Hitung", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("✕  Hapus", use_container_width=True)

    if clear_btn:
        st.session_state.last_result = None
        st.rerun()

    if calc_btn:
        with st.spinner("Menghitung..."):
            pb = binomial_pb(float(A), int(S), int(N))

        if pb is None:
            st.markdown(
                '<div class="warn-box">⚠ Perhitungan gagal — nilai terlalu besar untuk kalkulasi faktorial. '
                'Coba kurangi nilai S.</div>',
                unsafe_allow_html=True
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
            st.success(f"✓ Berhasil dihitung — total {len(st.session_state.history)} data tersimpan")

    if st.session_state.last_result:
        r = st.session_state.last_result
        gos, badge_cls = grade_of_service(r["Pb"])
        st.markdown('<div class="section-header">Hasil Cepat</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card" style="display:flex; gap:2rem; align-items:center; flex-wrap:wrap;">
            <div>
                <div class="result-big">{r['Pb']*100:.4f}%</div>
                <div class="result-label">Probabilitas Blokir (Pb)</div>
            </div>
            <div style="flex:1;">
                <div class="metric-row">
                    <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A (Erlang/Sumber)</div></div>
                    <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S (Sumber)</div></div>
                    <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N (Server)</div></div>
                    <div class="metric-tile"><div class="val"><span class="badge {badge_cls}">{gos}</span></div><div class="lbl">Kelas Layanan</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HASIL
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Hasil":

    st.markdown('<div class="app-title">Hasil Perhitungan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Rincian lengkap hasil komputasi terakhir beserta grafik analisis</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.last_result:
        st.markdown(
            '<div class="info-box">ℹ Belum ada perhitungan. Pergi ke tab <b>Kalkulator</b> dan '
            'jalankan perhitungan terlebih dahulu.</div>',
            unsafe_allow_html=True
        )
    else:
        r = st.session_state.last_result
        pb = r["Pb"]
        gos, badge_cls = grade_of_service(pb)
        total_traffic  = r['A'] * r['S']
        offered_load   = total_traffic
        carried_load   = total_traffic * (1 - pb)
        blocked_traffic = total_traffic * pb

        # ── Hasil Utama ──
        st.markdown('<div class="section-header">Hasil Utama</div>', unsafe_allow_html=True)
        notes_html = f"<div class='result-sub'><i>{r['Notes']}</i></div>" if r.get("Notes") else ""
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex; align-items:flex-start; gap:2.5rem; flex-wrap:wrap;">
                <div>
                    <div class="result-big">{pb*100:.6f}%</div>
                    <div class="result-label">Probabilitas Blokir (Pb)</div>
                    <div style="margin-top:0.6rem;">
                        <span class="badge {badge_cls}">{gos}</span>
                        &nbsp;<span style="font-size:0.78rem;color:#8b949e;font-family:'IBM Plex Mono',monospace;">Kelas Layanan</span>
                    </div>
                    <div class="result-sub">Nilai desimal: <code style="color:#58a6ff;">{pb:.8f}</code></div>
                    <div class="result-sub">Dicatat: <code style="font-size:0.8rem;color:#8b949e;">{r['Timestamp']}</code></div>
                    {notes_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Parameter Masukan ──
        st.markdown('<div class="section-header">Parameter Masukan</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A — Erlang/Sumber</div></div>
            <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S — Jumlah Sumber</div></div>
            <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N — Jumlah Server</div></div>
            <div class="metric-tile"><div class="val">{r['S'] - r['N']}</div><div class="lbl">S - N (Sumber Lebih)</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Metrik Trafik ──
        st.markdown('<div class="section-header">Metrik Trafik Turunan</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{offered_load:.4f}</div><div class="lbl">Total Ditawarkan (Erl)</div></div>
            <div class="metric-tile"><div class="val">{carried_load:.4f}</div><div class="lbl">Beban Dilayani (Erl)</div></div>
            <div class="metric-tile"><div class="val">{blocked_traffic:.4f}</div><div class="lbl">Trafik Terblokir (Erl)</div></div>
            <div class="metric-tile"><div class="val">{(1-pb)*100:.4f}%</div><div class="lbl">Tingkat Throughput</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ══════════════════════════════════════════════
        # GRAFIK ANALISIS
        # ══════════════════════════════════════════════
        st.markdown('<div class="section-header">Grafik Analisis</div>', unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        # ── Grafik 1: Donut Chart — Distribusi Trafik ──
        with chart_col1:
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Trafik Dilayani", "Trafik Terblokir"],
                values=[carried_load, blocked_traffic],
                hole=0.55,
                marker=dict(
                    colors=["#3fb950", "#f78166"],
                    line=dict(color="#0d1117", width=2)
                ),
                textinfo="label+percent",
                textfont=dict(family="IBM Plex Mono", size=12, color="#e6edf3"),
                hovertemplate="<b>%{label}</b><br>%{value:.4f} Erl<br>%{percent}<extra></extra>",
            )])
            fig_donut.update_layout(
                title=dict(
                    text="Distribusi Beban Trafik",
                    font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                    x=0.5
                ),
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font=dict(color="#e6edf3"),
                legend=dict(
                    font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    bgcolor="rgba(0,0,0,0)",
                    orientation="h",
                    yanchor="bottom", y=-0.15,
                    xanchor="center", x=0.5
                ),
                margin=dict(t=50, b=40, l=20, r=20),
                height=320,
                annotations=[dict(
                    text=f"<b>{(1-pb)*100:.1f}%</b><br>Throughput",
                    x=0.5, y=0.5, font_size=13,
                    font=dict(family="IBM Plex Mono", color="#e6edf3"),
                    showarrow=False
                )]
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

        # ── Grafik 2: Bar Chart — Pb vs N (Sensitivitas Server) ──
        with chart_col2:
            n_vals = list(range(max(1, r['N'] - 4), min(r['S'], r['N'] + 6)))
            pb_vals = []
            for nv in n_vals:
                pv = binomial_pb(r['A'], r['S'], nv)
                pb_vals.append((pv * 100) if pv is not None else None)

            bar_colors = [
                "#58a6ff" if nv == r['N'] else "#30363d"
                for nv in n_vals
            ]

            fig_bar = go.Figure(data=[go.Bar(
                x=[str(nv) for nv in n_vals],
                y=pb_vals,
                marker=dict(color=bar_colors, line=dict(color="#0d1117", width=1)),
                hovertemplate="<b>N = %{x}</b><br>Pb = %{y:.4f}%<extra></extra>",
                text=[f"{v:.3f}%" if v is not None else "N/A" for v in pb_vals],
                textposition="outside",
                textfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
            )])
            fig_bar.update_layout(
                title=dict(
                    text="Sensitivitas Pb terhadap Jumlah Server (N)",
                    font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                    x=0.5
                ),
                xaxis=dict(
                    title="Jumlah Server (N)",
                    title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    gridcolor="#21262d", linecolor="#30363d"
                ),
                yaxis=dict(
                    title="Pb (%)",
                    title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    gridcolor="#21262d", linecolor="#30363d"
                ),
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                margin=dict(t=55, b=50, l=50, r=20),
                height=320,
                annotations=[dict(
                    text=f"▲ N saat ini = {r['N']}",
                    xref="paper", yref="paper",
                    x=0.99, y=0.99, showarrow=False,
                    font=dict(family="IBM Plex Mono", size=10, color="#58a6ff"),
                    align="right"
                )]
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

        # ── Grafik 3: Kurva Pb vs A (Pengaruh Intensitas Trafik) ──
        st.markdown(
            '<div class="section-header">Kurva Pb vs Intensitas Trafik (A)</div>',
            unsafe_allow_html=True
        )
        a_range = [round(i * 0.01, 2) for i in range(1, 100)]
        pb_curve = []
        for av in a_range:
            pv = binomial_pb(av, r['S'], r['N'])
            pb_curve.append((pv * 100) if pv is not None else None)

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=a_range,
            y=pb_curve,
            mode="lines",
            name="Pb (%)",
            line=dict(color="#58a6ff", width=2.5),
            hovertemplate="A = %{x:.2f}<br>Pb = %{y:.4f}%<extra></extra>",
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)"
        ))
        # Titik nilai saat ini
        fig_line.add_trace(go.Scatter(
            x=[r['A']],
            y=[pb * 100],
            mode="markers",
            name=f"Nilai Saat Ini (A={r['A']})",
            marker=dict(color="#3fb950", size=10, symbol="circle",
                        line=dict(color="#0d1117", width=2)),
            hovertemplate=f"A = {r['A']}<br>Pb = {pb*100:.4f}%<extra></extra>",
        ))
        # Garis batas GoS
        fig_line.add_hline(y=1.0, line_dash="dot", line_color="#ffa600", line_width=1,
                           annotation_text="Batas GoS 1%", annotation_font_color="#ffa600",
                           annotation_font_size=10, annotation_position="top right")
        fig_line.add_hline(y=5.0, line_dash="dot", line_color="#f78166", line_width=1,
                           annotation_text="Batas GoS 5%", annotation_font_color="#f78166",
                           annotation_font_size=10, annotation_position="top right")

        fig_line.update_layout(
            title=dict(
                text=f"Probabilitas Blokir (Pb) vs Intensitas Trafik per Sumber (A)  |  S={r['S']}, N={r['N']}",
                font=dict(family="IBM Plex Mono", size=13, color="#e6edf3"),
                x=0.5
            ),
            xaxis=dict(
                title="Intensitas Trafik per Sumber (A)",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                gridcolor="#21262d", linecolor="#30363d",
                range=[0, 1]
            ),
            yaxis=dict(
                title="Probabilitas Blokir Pb (%)",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                gridcolor="#21262d", linecolor="#30363d"
            ),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            legend=dict(
                font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                bgcolor="rgba(22,27,34,0.9)",
                bordercolor="#30363d", borderwidth=1
            ),
            margin=dict(t=60, b=50, l=60, r=30),
            height=350,
        )
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

        # ── Grafik 4: Heatmap Pb vs (N, S) ──
        st.markdown(
            '<div class="section-header">Peta Panas Pb — Jumlah Server vs Sumber</div>',
            unsafe_allow_html=True
        )
        s_range = list(range(max(2, r['S'] - 5), min(51, r['S'] + 6)))
        n_range = list(range(1, min(r['S'] + 5, 20)))
        heat_z = []
        for sv in s_range:
            row_data = []
            for nv in n_range:
                if nv >= sv:
                    row_data.append(0.0)
                else:
                    pv = binomial_pb(r['A'], sv, nv)
                    row_data.append((pv * 100) if pv is not None else 0.0)
            heat_z.append(row_data)

        fig_heat = go.Figure(data=go.Heatmap(
            z=heat_z,
            x=[str(nv) for nv in n_range],
            y=[str(sv) for sv in s_range],
            colorscale=[[0, "#0d1117"], [0.2, "#1f4068"], [0.5, "#58a6ff"], [0.8, "#ffa600"], [1, "#f78166"]],
            hovertemplate="N = %{x}<br>S = %{y}<br>Pb = %{z:.4f}%<extra></extra>",
            colorbar=dict(
                title="Pb (%)",
                titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                bgcolor="#161b22",
                bordercolor="#30363d",
            )
        ))
        # Tandai posisi saat ini
        fig_heat.add_trace(go.Scatter(
            x=[str(r['N'])],
            y=[str(r['S'])],
            mode="markers",
            marker=dict(symbol="x", size=14, color="#3fb950",
                        line=dict(color="#0d1117", width=2)),
            name="Posisi Saat Ini",
            hovertemplate=f"N={r['N']}, S={r['S']}<br>Pb={pb*100:.4f}%<extra></extra>"
        ))
        fig_heat.update_layout(
            title=dict(
                text=f"Peta Panas Pb (%)  |  A={r['A']}",
                font=dict(family="IBM Plex Mono", size=13, color="#e6edf3"),
                x=0.5
            ),
            xaxis=dict(
                title="Jumlah Server (N)",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
            ),
            yaxis=dict(
                title="Jumlah Sumber (S)",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
            ),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            legend=dict(
                font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                bgcolor="rgba(22,27,34,0.9)",
                bordercolor="#30363d", borderwidth=1
            ),
            margin=dict(t=60, b=50, l=60, r=20),
            height=360,
        )
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

        # ── Analisis Sensitivitas ──
        st.markdown(
            '<div class="section-header">Analisis Sensitivitas — Tambah 1 Server</div>',
            unsafe_allow_html=True
        )
        pb_plus1 = binomial_pb(r['A'], r['S'], r['N'] + 1)
        if pb_plus1 is not None and r['N'] + 1 < r['S']:
            delta = pb - pb_plus1
            gos2, badge2 = grade_of_service(pb_plus1)
            st.markdown(f"""
            <div class="info-box">
            Menambah 1 server (N → <b>{r['N']+1}</b>) akan menurunkan Pb dari
            <b>{pb*100:.4f}%</b> menjadi <b>{pb_plus1*100:.4f}%</b>
            &nbsp;(Δ = −{delta*100:.4f} pp) &nbsp; <span class="badge {badge2}">{gos2}</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Langkah Formula ──
        with st.expander("📐 Penjelasan Langkah Formula"):
            st.markdown(f"""
            **Rumus Blokir Binomial:**

            ```
            Pb = Σ(x = N to S-1) [ (S-1)! / (x! · (S-1-x)!) ] · A^x · (1-A)^(S-1-x)
            ```

            **Dengan nilai Anda** — A = {r['A']}, S = {r['S']}, N = {r['N']}:

            - Penjumlahan dari x = **{r['N']}** hingga x = **{r['S']-1}**
            - Total suku yang dievaluasi: **{r['S'] - r['N']}**
            - S-1 = **{r['S']-1}**, (1-A) = **{1-r['A']:.4f}**

            Setiap suku mewakili probabilitas bahwa tepat *x* dari *S-1* sumber
            aktif secara bersamaan, dibobot dengan koefisien binomial.
            Jumlahnya memberikan total probabilitas bahwa semua N server terpakai
            saat panggilan baru tiba.
            """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RIWAYAT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Riwayat":

    st.markdown('<div class="app-title">Riwayat Perhitungan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Semua komputasi dalam sesi ini</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.history:
        st.markdown(
            '<div class="info-box">ℹ Belum ada riwayat. Jalankan perhitungan di tab <b>Kalkulator</b>.</div>',
            unsafe_allow_html=True
        )
    else:
        n = len(st.session_state.history)
        pbs = [r["Pb"] for r in st.session_state.history]

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{n}</div><div class="lbl">Total Data</div></div>
            <div class="metric-tile"><div class="val">{min(pbs)*100:.4f}%</div><div class="lbl">Pb Minimum</div></div>
            <div class="metric-tile"><div class="val">{max(pbs)*100:.4f}%</div><div class="lbl">Pb Maksimum</div></div>
            <div class="metric-tile"><div class="val">{sum(pbs)/n*100:.4f}%</div><div class="lbl">Rata-rata Pb</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Data Tersimpan</div>', unsafe_allow_html=True)

        rows = []
        for i, rec in enumerate(reversed(st.session_state.history), 1):
            gos, _ = grade_of_service(rec["Pb"])
            rows.append({
                "#": n - i + 1,
                "Waktu": rec["Timestamp"],
                "A": rec["A"],
                "S": rec["S"],
                "N": rec["N"],
                "Pb (Desimal)": f"{rec['Pb']:.8f}",
                "Pb (%)": f"{rec['Pb']*100:.4f}%",
                "Kelas Layanan": gos,
                "Catatan": rec.get("Notes", ""),
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Grafik Tren Riwayat ──
        st.markdown('<div class="section-header">Grafik Tren Probabilitas Blokir</div>', unsafe_allow_html=True)

        hist_df = pd.DataFrame({
            "No": list(range(1, n + 1)),
            "Pb (%)": [r["Pb"] * 100 for r in st.session_state.history],
            "A": [r["A"] for r in st.session_state.history],
            "S": [r["S"] for r in st.session_state.history],
            "N": [r["N"] for r in st.session_state.history],
            "Kelas Layanan": [grade_of_service(r["Pb"])[0] for r in st.session_state.history],
            "Waktu": [r["Timestamp"] for r in st.session_state.history],
        })

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=hist_df["No"],
            y=hist_df["Pb (%)"],
            mode="lines+markers",
            name="Pb (%)",
            line=dict(color="#58a6ff", width=2),
            marker=dict(size=7, color="#58a6ff", line=dict(color="#0d1117", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)",
            hovertemplate=(
                "<b>Data ke-%{x}</b><br>"
                "Pb = %{y:.4f}%<br>"
                "<extra></extra>"
            ),
        ))
        fig_trend.add_hline(y=1.0, line_dash="dot", line_color="#ffa600", line_width=1,
                            annotation_text="GoS 1%", annotation_font_color="#ffa600",
                            annotation_font_size=10, annotation_position="top right")
        fig_trend.add_hline(y=5.0, line_dash="dot", line_color="#f78166", line_width=1,
                            annotation_text="GoS 5%", annotation_font_color="#f78166",
                            annotation_font_size=10, annotation_position="top right")
        fig_trend.update_layout(
            title=dict(
                text="Tren Pb Sepanjang Sesi",
                font=dict(family="IBM Plex Mono", size=13, color="#e6edf3"),
                x=0.5
            ),
            xaxis=dict(
                title="Nomor Data",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                gridcolor="#21262d", linecolor="#30363d",
                dtick=1
            ),
            yaxis=dict(
                title="Pb (%)",
                title_font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                gridcolor="#21262d", linecolor="#30363d"
            ),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            margin=dict(t=55, b=50, l=60, r=30),
            height=300,
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

        # ── Ekspor ──
        st.markdown('<div class="section-header">Ekspor Data</div>', unsafe_allow_html=True)
        col_dl1, col_dl2, col_clr, _ = st.columns([1.2, 1.2, 1, 3])

        with col_dl1:
            try:
                from fpdf import FPDF  # noqa: F401
                pdf_bytes = generate_pdf(st.session_state.history)
                file_ext = "pdf"
                mime_type = "application/pdf"
                btn_label = "⬇  Unduh PDF"
            except ImportError:
                pdf_bytes = generate_pdf(st.session_state.history)
                file_ext = "txt"
                mime_type = "text/plain"
                btn_label = "⬇  Unduh TXT"

            st.download_button(
                label=btn_label,
                data=pdf_bytes,
                file_name=f"riwayat_binomial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                mime=mime_type,
                use_container_width=True,
            )

        with col_dl2:
            csv_rows = ["Waktu,A,S,N,Pb,Pb(%),Kelas Layanan,Catatan"]
            for rec in st.session_state.history:
                gos, _ = grade_of_service(rec["Pb"])
                csv_rows.append(
                    f"{rec['Timestamp']},{rec['A']},{rec['S']},{rec['N']},"
                    f"{rec['Pb']:.8f},{rec['Pb']*100:.4f}%,{gos},{rec.get('Notes','')}"
                )
            csv_data = "\n".join(csv_rows)
            st.download_button(
                label="⬇  Unduh CSV",
                data=csv_data.encode("utf-8"),
                file_name=f"riwayat_binomial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col_clr:
            if st.button("🗑  Hapus Semua", use_container_width=True):
                st.session_state.history = []
                st.session_state.last_result = None
                st.rerun()
