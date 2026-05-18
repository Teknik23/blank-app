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

# ─── CSS Kustom ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

/* ── Tema utama ── */
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

/* ── Kontainer utama ── */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1100px;
}

/* ── Judul halaman ── */
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

/* ── Header seksi ── */
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

/* ── Kartu hasil ── */
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

/* ── Kotak metrik ── */
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

/* ── Tampilan rumus ── */
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

/* ── Tabel riwayat ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 6px; }

/* ── Tombol ── */
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

/* ── Tombol unduh ── */
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

/* ── Input ── */
.stNumberInput input, .stSlider {
    font-family: var(--mono);
}

/* ── Kotak info / peringatan ── */
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

/* ── Label status ── */
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

/* ── Tombol navigasi sidebar ── */
div[data-testid="stVerticalBlock"] .stRadio > div { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)


# ─── Fungsi Perhitungan Utama ────────────────────────────────────────────────────
def binomial_pb(A: float, S: int, N: int):
    """
    Pb = Σ(x=N to S-1) [ (S-1)! / (x! * (S-1-X)!) ] * A^x * (1-A)^(S-1-X)

    A = Trafik yang ditawarkan per sumber (Erlang)
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


# ─── Fungsi Generate PDF ─────────────────────────────────────────────────────────
def _safe(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-",
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00d7": "x",
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
            _safe("Rumus: Pb = JUMLAH(x=N hingga S-1) [ (S-1)! / (x!(S-1-X)!) ] * A^x * (1-A)^(S-1-X)\n"
            "Keterangan: A = Erlang/sumber, S = Sumber, N = Server, Pb = Probabilitas pemblokiran"),
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
                str(row['A']),
                str(row['S']),
                str(row['N']),
                pb_pct,
                gos,
                row.get("Notes", ""),
            ]
            for i, v in enumerate(vals):
                pdf.cell(col_w[i], 6, _safe(v), border=1, fill=fill, align="C" if i != 6 else "L")
            pdf.ln()

        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, _safe("Kalkulator Trafik Binomial - Alat Rekayasa Teletrafik"), align="C")

        result = pdf.output()
        if isinstance(result, (bytes, bytearray)):
            return bytes(result)
        return result.encode("latin-1")

    except ImportError:
        lines = [
            "Kalkulator Trafik Binomial - Laporan Riwayat",
            f"Dibuat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "",
            "Waktu,A,S,N,Pb,Pb(%),GoS,Catatan"
        ]
        for r in history:
            gos, _ = grade_of_service(r['Pb'])
            lines.append(f"{r.get('Timestamp','')},{r['A']},{r['S']},{r['N']},"
                         f"{r['Pb']:.6f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}")
        return "\n".join(lines).encode("utf-8")


# ─── Inisialisasi State Sesi ─────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Kalkulator"


# ─── Navigasi Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">📡 Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Kalkulator Teletrafik</div>', unsafe_allow_html=True)

    tab = st.radio(
        "Navigasi",
        ["🧮  Kalkulator", "📊  Hasil", "🗂️  Riwayat"],
        label_visibility="collapsed",
    )
    # Ambil nama tab dengan aman
    st.session_state.active_tab = tab.split("  ", 1)[1] if "  " in tab else tab.split(" ", 1)[1]

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#8b949e; line-height:1.7; font-family:'IBM Plex Mono',monospace;">
    <b style="color:#58a6ff;">VARIABEL</b><br>
    <b>A</b> — Erlang / sumber<br>
    <b>S</b> — Total sumber<br>
    <b>N</b> — Server (sirkuit)<br>
    <b>Pb</b> — Prob. pemblokiran<br><br>
    <b style="color:#58a6ff;">RUMUS</b><br>
    Model sumber terbatas<br>
    kelas Engset dengan<br>
    asumsi percobaan ulang.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        st.markdown(
            f'<div style="font-size:0.75rem;color:#8b949e;font-family:\'IBM Plex Mono\',monospace;">'
            f'📋 {len(st.session_state.history)} data tersimpan</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KALKULATOR
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Kalkulator":

    st.markdown('<div class="app-title">Kalkulator Trafik Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Probabilitas pemblokiran sumber terbatas — Model Binomial</div>', unsafe_allow_html=True)

    # Kotak rumus
    st.markdown("""
    <div class="formula-box">
    <span class="hi">Pb</span> = Σ <sub>x=N</sub><sup>S-1</sup>
    &nbsp; <span class="hi2">(S-1)!</span> / [x!(S-1-X)!]
    &nbsp;·&nbsp; <span class="hi">A</span><sup>x</sup>
    &nbsp;·&nbsp; (1-<span class="hi">A</span>)<sup>(S-1-X)</sup>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Parameter Masukan</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        A = st.number_input(
            "A — Erlang yang Ditawarkan per Sumber",
            min_value=0.001, max_value=0.999,
            value=0.1, step=0.001, format="%.4f",
            help="Intensitas trafik yang ditawarkan oleh setiap sumber individu (0 < A < 1)"
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

    # Validasi
    if N >= S:
        st.markdown(
            f'<div class="warn-box">⚠ N harus lebih kecil dari S. Saat ini N={N} ≥ S={S}. Pb akan bernilai 0 (tidak ada pemblokiran).</div>',
            unsafe_allow_html=True
        )

    # Catatan
    notes = st.text_input(
        "Catatan (opsional)",
        placeholder="mis. Skenario A — trafik jam sibuk",
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
                '<div class="warn-box">⚠ Perhitungan gagal — nilai mungkin terlalu besar untuk kalkulasi faktorial. Coba kurangi nilai S.</div>',
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
            st.success(f"✓ Berhasil dihitung — {len(st.session_state.history)} total data")

    # Tampilkan ringkasan hasil terakhir
    if st.session_state.last_result:
        r = st.session_state.last_result
        gos, badge_cls = grade_of_service(r["Pb"])
        st.markdown('<div class="section-header">Hasil Cepat</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card" style="display:flex; gap:2rem; align-items:center; flex-wrap:wrap;">
            <div>
                <div class="result-big">{r['Pb']*100:.4f}%</div>
                <div class="result-label">Probabilitas Pemblokiran (Pb)</div>
            </div>
            <div style="flex:1;">
                <div class="metric-row">
                    <div class="metric-tile"><div class="val">{r['A']}</div><div class="lbl">A (Erlang/sumber)</div></div>
                    <div class="metric-tile"><div class="val">{r['S']}</div><div class="lbl">S (Sumber)</div></div>
                    <div class="metric-tile"><div class="val">{r['N']}</div><div class="lbl">N (Server)</div></div>
                    <div class="metric-tile"><div class="val"><span class="badge {badge_cls}">{gos}</span></div><div class="lbl">Grade of Service</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HASIL
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Hasil":

    st.markdown('<div class="app-title">Hasil Perhitungan</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Rincian lengkap dari komputasi terakhir</div>', unsafe_allow_html=True)

    if not st.session_state.last_result:
        st.markdown(
            '<div class="info-box">ℹ Belum ada perhitungan. Pergi ke tab <b>Kalkulator</b> dan jalankan perhitungan terlebih dahulu.</div>',
            unsafe_allow_html=True
        )
    else:
        r = st.session_state.last_result
        pb = r["Pb"]
        gos, badge_cls = grade_of_service(pb)
        total_traffic = r['A'] * r['S']
        offered_load  = total_traffic
        carried_load  = total_traffic * (1 - pb)
        blocked_calls = total_traffic * pb

        # ── Hasil Utama ──
        st.markdown('<div class="section-header">Hasil Utama</div>', unsafe_allow_html=True)
        notes_html = f"<div class='result-sub'><i>{r['Notes']}</i></div>" if r.get('Notes') else ""
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex; align-items:flex-start; gap:2.5rem; flex-wrap:wrap;">
                <div>
                    <div class="result-big">{pb*100:.6f}%</div>
                    <div class="result-label">Probabilitas Pemblokiran (Pb)</div>
                    <div style="margin-top:0.6rem;">
                        <span class="badge {badge_cls}">{gos}</span>
                        &nbsp;<span style="font-size:0.78rem;color:#8b949e;font-family:'IBM Plex Mono',monospace;">Grade of Service</span>
                    </div>
                    <div class="result-sub">Dalam desimal: <code style="color:#58a6ff;">{pb:.8f}</code></div>
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
            <div class="metric-tile"><div class="val">{r['S'] - r['N']}</div><div class="lbl">S - N (Sumber Berlebih)</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Metrik Trafik Turunan ──
        st.markdown('<div class="section-header">Metrik Trafik Turunan</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{offered_load:.4f}</div><div class="lbl">Total Ditawarkan (Erl)</div></div>
            <div class="metric-tile"><div class="val">{carried_load:.4f}</div><div class="lbl">Beban Terlayani (Erl)</div></div>
            <div class="metric-tile"><div class="val">{blocked_calls:.4f}</div><div class="lbl">Trafik Terblokir (Erl)</div></div>
            <div class="metric-tile"><div class="val">{(1-pb)*100:.4f}%</div><div class="lbl">Tingkat Throughput</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ════════════════════════════════════════════
        # GRAFIK HASIL
        # ════════════════════════════════════════════
        st.markdown('<div class="section-header">Visualisasi Grafik</div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)

        # ── Grafik 1: Komposisi Trafik (Donut) ──
        with col_g1:
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Trafik Terlayani", "Trafik Terblokir"],
                values=[carried_load, blocked_calls],
                hole=0.55,
                marker=dict(
                    colors=["#3fb950", "#f78166"],
                    line=dict(color="#0d1117", width=2)
                ),
                textinfo="label+percent",
                textfont=dict(family="IBM Plex Mono", size=12, color="#e6edf3"),
                hovertemplate="<b>%{label}</b><br>Nilai: %{value:.4f} Erl<br>Porsi: %{percent}<extra></extra>",
            )])
            fig_donut.update_layout(
                title=dict(
                    text="Komposisi Trafik",
                    font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                    x=0.5
                ),
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font=dict(color="#e6edf3"),
                legend=dict(
                    font=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                    borderwidth=1,
                ),
                margin=dict(t=60, b=20, l=20, r=20),
                height=300,
                annotations=[dict(
                    text=f"{pb*100:.2f}%<br><span style='font-size:10px'>Pb</span>",
                    x=0.5, y=0.5,
                    font=dict(size=16, family="IBM Plex Mono", color="#e6edf3"),
                    showarrow=False
                )]
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

        # ── Grafik 2: Pb vs Jumlah Server (Sensitivitas) ──
        with col_g2:
            n_range = list(range(1, min(r['S'], r['N'] + 8)))
            pb_vals = []
            for n_i in n_range:
                val = binomial_pb(r['A'], r['S'], n_i)
                pb_vals.append((val * 100) if val is not None else None)

            fig_sens = go.Figure()
            fig_sens.add_trace(go.Scatter(
                x=n_range,
                y=pb_vals,
                mode="lines+markers",
                line=dict(color="#58a6ff", width=2.5),
                marker=dict(
                    size=7,
                    color=["#f78166" if n_i == r['N'] else "#58a6ff" for n_i in n_range],
                    line=dict(color="#0d1117", width=1.5)
                ),
                hovertemplate="<b>N = %{x}</b><br>Pb = %{y:.4f}%<extra></extra>",
                name="Pb (%)"
            ))
            # Tandai titik aktif
            fig_sens.add_trace(go.Scatter(
                x=[r['N']],
                y=[pb * 100],
                mode="markers",
                marker=dict(size=13, color="#f78166", symbol="diamond",
                            line=dict(color="#e6edf3", width=1.5)),
                hovertemplate=f"<b>N saat ini = {r['N']}</b><br>Pb = {pb*100:.4f}%<extra></extra>",
                name=f"N Aktif ({r['N']})"
            ))
            # Garis batas GoS
            fig_sens.add_hline(y=1.0, line_dash="dot", line_color="#ffa600",
                               annotation_text="Batas 1%", annotation_position="right",
                               annotation_font=dict(color="#ffa600", size=10, family="IBM Plex Mono"))
            fig_sens.add_hline(y=5.0, line_dash="dot", line_color="#f78166",
                               annotation_text="Batas 5%", annotation_position="right",
                               annotation_font=dict(color="#f78166", size=10, family="IBM Plex Mono"))
            fig_sens.update_layout(
                title=dict(
                    text="Pb vs Jumlah Server (N)",
                    font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                    x=0.5
                ),
                xaxis=dict(
                    title="Jumlah Server (N)",
                    titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                    gridcolor="#21262d", zeroline=False, showline=True,
                    linecolor="#30363d"
                ),
                yaxis=dict(
                    title="Pb (%)",
                    titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                    tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                    gridcolor="#21262d", zeroline=False, showline=True,
                    linecolor="#30363d"
                ),
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                legend=dict(
                    font=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                    bgcolor="#161b22", bordercolor="#30363d", borderwidth=1
                ),
                margin=dict(t=60, b=50, l=60, r=80),
                height=300,
            )
            st.plotly_chart(fig_sens, use_container_width=True, config={"displayModeBar": False})

        # ── Grafik 3: Pb vs Nilai A (Trafik per Sumber) ──
        st.markdown('<div class="section-header">Sensitivitas terhadap Nilai A</div>', unsafe_allow_html=True)
        a_range = [round(0.01 * i, 2) for i in range(1, 99)]
        pb_a_vals = []
        for a_i in a_range:
            val = binomial_pb(a_i, r['S'], r['N'])
            pb_a_vals.append((val * 100) if val is not None else None)

        fig_a = go.Figure()
        fig_a.add_trace(go.Scatter(
            x=a_range,
            y=pb_a_vals,
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)",
            line=dict(color="#58a6ff", width=2.5),
            hovertemplate="<b>A = %{x:.2f}</b><br>Pb = %{y:.4f}%<extra></extra>",
            name="Pb (%)"
        ))
        # Tandai nilai A aktif
        pb_current_a = binomial_pb(r['A'], r['S'], r['N'])
        if pb_current_a is not None:
            fig_a.add_trace(go.Scatter(
                x=[r['A']],
                y=[pb_current_a * 100],
                mode="markers",
                marker=dict(size=12, color="#f78166", symbol="diamond",
                            line=dict(color="#e6edf3", width=1.5)),
                hovertemplate=f"<b>A saat ini = {r['A']}</b><br>Pb = {pb_current_a*100:.4f}%<extra></extra>",
                name=f"A Aktif ({r['A']})"
            ))
        fig_a.add_hline(y=1.0, line_dash="dot", line_color="#ffa600",
                        annotation_text="Batas 1%", annotation_position="right",
                        annotation_font=dict(color="#ffa600", size=10, family="IBM Plex Mono"))
        fig_a.add_hline(y=5.0, line_dash="dot", line_color="#f78166",
                        annotation_text="Batas 5%", annotation_position="right",
                        annotation_font=dict(color="#f78166", size=10, family="IBM Plex Mono"))
        fig_a.update_layout(
            title=dict(
                text=f"Pb vs Nilai A  (S={r['S']}, N={r['N']} tetap)",
                font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                x=0.5
            ),
            xaxis=dict(
                title="A — Erlang per Sumber",
                titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                gridcolor="#21262d", zeroline=False, showline=True, linecolor="#30363d"
            ),
            yaxis=dict(
                title="Pb (%)",
                titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                gridcolor="#21262d", zeroline=False, showline=True, linecolor="#30363d"
            ),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            legend=dict(
                font=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                bgcolor="#161b22", bordercolor="#30363d", borderwidth=1
            ),
            margin=dict(t=60, b=50, l=60, r=80),
            height=320,
        )
        st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})

        # ── Analisis Sensitivitas +1 Server ──
        st.markdown('<div class="section-header">Analisis Sensitivitas — Tambah 1 Server</div>', unsafe_allow_html=True)
        pb_plus1 = binomial_pb(r['A'], r['S'], r['N'] + 1)
        if pb_plus1 is not None and r['N'] + 1 < r['S']:
            delta = pb - pb_plus1
            gos2, badge2 = grade_of_service(pb_plus1)
            st.markdown(f"""
            <div class="info-box">
            Menambah 1 server (N → <b>{r['N']+1}</b>) akan mengurangi Pb dari
            <b>{pb*100:.4f}%</b> menjadi <b>{pb_plus1*100:.4f}%</b>
            &nbsp;(Δ = −{delta*100:.4f} pp) &nbsp; <span class="badge {badge2}">{gos2}</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Penjelasan Rumus ──
        with st.expander("📐 Penjelasan Rumus"):
            st.markdown(f"""
            **Rumus Pemblokiran Binomial:**

            ```
            Pb = Σ(x = N hingga S-1) [ (S-1)! / (x! · (S-1-x)!) ] · A^x · (1-A)^(S-1-x)
            ```

            **Dengan nilai Anda** — A = {r['A']}, S = {r['S']}, N = {r['N']}:

            - Penjumlahan berjalan dari x = **{r['N']}** hingga x = **{r['S']-1}**
            - Total suku yang dievaluasi: **{r['S'] - r['N']}**
            - S-1 = **{r['S']-1}**, (1-A) = **{1-r['A']:.4f}**

            Setiap suku mewakili probabilitas bahwa tepat *x* dari *S-1* sumber aktif secara bersamaan,
            dikalikan dengan koefisien binomial. Jumlahnya memberikan total probabilitas bahwa semua
            server N sedang terisi saat panggilan baru tiba.
            """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RIWAYAT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Riwayat":

    st.markdown('<div class="app-title">Riwayat Perhitungan</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Semua komputasi dalam sesi ini</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div class="info-box">ℹ Belum ada riwayat. Jalankan perhitungan di tab <b>Kalkulator</b>.</div>',
            unsafe_allow_html=True
        )
    else:
        n = len(st.session_state.history)
        pbs = [r["Pb"] for r in st.session_state.history]

        # Baris statistik ringkasan
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-tile"><div class="val">{n}</div><div class="lbl">Total Data</div></div>
            <div class="metric-tile"><div class="val">{min(pbs)*100:.4f}%</div><div class="lbl">Pb Minimum</div></div>
            <div class="metric-tile"><div class="val">{max(pbs)*100:.4f}%</div><div class="lbl">Pb Maksimum</div></div>
            <div class="metric-tile"><div class="val">{sum(pbs)/n*100:.4f}%</div><div class="lbl">Pb Rata-rata</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Data Riwayat</div>', unsafe_allow_html=True)

        # Buat dataframe
        rows = []
        for i, r in enumerate(reversed(st.session_state.history), 1):
            gos, _ = grade_of_service(r["Pb"])
            rows.append({
                "#": n - i + 1,
                "Waktu": r["Timestamp"],
                "A": r["A"],
                "S": r["S"],
                "N": r["N"],
                "Pb (desimal)": f"{r['Pb']:.8f}",
                "Pb (%)": f"{r['Pb']*100:.4f}%",
                "GoS": gos,
                "Catatan": r.get("Notes", ""),
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

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
            csv_rows = ["Waktu,A,S,N,Pb,Pb(%),GoS,Catatan"]
            for r in st.session_state.history:
                gos, _ = grade_of_service(r["Pb"])
                csv_rows.append(
                    f"{r['Timestamp']},{r['A']},{r['S']},{r['N']},"
                    f"{r['Pb']:.8f},{r['Pb']*100:.4f}%,{gos},{r.get('Notes','')}"
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

        # ── Grafik Tren di Riwayat ──
        st.markdown('<div class="section-header">Tren Probabilitas Pemblokiran</div>', unsafe_allow_html=True)

        records = list(range(1, n + 1))
        pb_pct_list = [r["Pb"] * 100 for r in st.session_state.history]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=records,
            y=pb_pct_list,
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.07)",
            line=dict(color="#58a6ff", width=2.5),
            marker=dict(size=8, color="#58a6ff", line=dict(color="#0d1117", width=1.5)),
            hovertemplate="<b>Data ke-%{x}</b><br>Pb = %{y:.4f}%<extra></extra>",
            name="Pb (%)"
        ))
        fig_trend.add_hline(y=1.0, line_dash="dot", line_color="#ffa600",
                            annotation_text="Batas 1%", annotation_position="right",
                            annotation_font=dict(color="#ffa600", size=10, family="IBM Plex Mono"))
        fig_trend.add_hline(y=5.0, line_dash="dot", line_color="#f78166",
                            annotation_text="Batas 5%", annotation_position="right",
                            annotation_font=dict(color="#f78166", size=10, family="IBM Plex Mono"))
        fig_trend.update_layout(
            title=dict(
                text="Tren Pb Sepanjang Sesi",
                font=dict(family="IBM Plex Mono", size=14, color="#e6edf3"),
                x=0.5
            ),
            xaxis=dict(
                title="Urutan Perhitungan",
                titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                gridcolor="#21262d", zeroline=False, showline=True, linecolor="#30363d",
                dtick=1
            ),
            yaxis=dict(
                title="Pb (%)",
                titlefont=dict(family="IBM Plex Mono", size=11, color="#8b949e"),
                tickfont=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                gridcolor="#21262d", zeroline=False, showline=True, linecolor="#30363d"
            ),
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            legend=dict(
                font=dict(family="IBM Plex Mono", size=10, color="#8b949e"),
                bgcolor="#161b22", bordercolor="#30363d", borderwidth=1
            ),
            margin=dict(t=60, b=50, l=60, r=80),
            height=300,
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
