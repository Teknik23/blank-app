import streamlit as st
import math
import pandas as pd
from datetime import datetime

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
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:       #0a0e17;
    --surface:  #111827;
    --card:     #1a2235;
    --border:   #1f2d45;
    --accent:   #38bdf8;
    --green:    #34d399;
    --warn:     #fb923c;
    --red:      #f87171;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --mono:     'Space Mono', monospace;
    --sans:     'DM Sans', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg) !important;
    color: var(--text);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

/* ── Main container ── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1200px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

/* ── Heading utama ── */
.page-title {
    font-family: var(--mono);
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
    line-height: 1.3;
}
.page-sub {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.3rem;
    margin-bottom: 1.8rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
}

/* ── Section label ── */
.sec-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    border-left: 3px solid var(--accent);
    padding-left: 0.6rem;
    margin: 1.6rem 0 0.9rem;
}

/* ── Kartu hasil utama ── */
.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin: 0.8rem 0;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--green));
}
.result-big {
    font-family: var(--mono);
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--green);
    letter-spacing: -1.5px;
    line-height: 1;
}
.result-label {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.result-sub {
    font-size: 0.84rem;
    color: var(--muted);
    margin-top: 0.6rem;
    font-family: var(--sans);
}

/* ── Tile metrik (dipakai via st.columns + HTML sederhana) ── */
.tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    transition: border-color 0.2s;
    height: 100%;
}
.tile:hover { border-color: var(--accent); }
.tile .tv {
    font-family: var(--mono);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
}
.tile .tl {
    font-size: 0.67rem;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 3px;
    font-family: var(--sans);
}

/* ── Kotak formula ── */
.formula-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.3rem;
    font-family: var(--mono);
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0.8rem 0 1.4rem;
    line-height: 2;
}
.formula-box .hl  { color: var(--accent); }
.formula-box .hl2 { color: var(--green); }

/* ── Info & peringatan ── */
.box-info {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.83rem;
    color: #94c4d8;
    margin: 0.7rem 0;
    font-family: var(--sans);
    line-height: 1.6;
}
.box-warn {
    background: rgba(251,146,60,0.07);
    border: 1px solid rgba(251,146,60,0.25);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.83rem;
    color: var(--warn);
    margin: 0.7rem 0;
    font-family: var(--sans);
    line-height: 1.6;
}
.box-err {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.25);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.83rem;
    color: var(--red);
    margin: 0.7rem 0;
    font-family: var(--sans);
    line-height: 1.6;
}

/* ── Badge status ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-family: var(--mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.badge-ok  { background: rgba(52,211,153,0.12); color: var(--green); border: 1px solid rgba(52,211,153,0.3); }
.badge-mid { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-bad { background: rgba(248,113,113,0.12); color: var(--red); border: 1px solid rgba(248,113,113,0.3); }

/* ── Tombol ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg) !important;
}

/* ── Tombol unduh ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--green) !important;
    color: var(--green) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: var(--green) !important;
    color: var(--bg) !important;
}

/* ── Input angka ── */
.stNumberInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    border-radius: 6px !important;
}
.stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
}
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

/* ── Tabel dataframe ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden;
}

/* ── Sidebar nav ── */
.stRadio > label { font-family: var(--sans) !important; color: var(--muted) !important; font-size: 0.85rem !important; }
.stRadio > div > label { padding: 0.3rem 0 !important; }

/* ── Label input ── */
.stNumberInput label, .stTextInput label, .stSlider label {
    font-family: var(--sans) !important;
    font-size: 0.83rem !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}

/* ── Expander ── */
.stExpander { border: 1px solid var(--border) !important; border-radius: 8px !important; }
.stExpander summary { font-family: var(--sans) !important; }

/* ── Alert streamlit ── */
.stAlert { border-radius: 8px !important; }

/* ── Sidebar logo ── */
.sidebar-brand {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.3px;
    padding: 0 0 0.2rem;
}
.sidebar-tagline {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--muted);
    margin-bottom: 1.2rem;
    letter-spacing: 0.5px;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0;
}
.sidebar-info {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--muted);
    line-height: 2;
}
.sidebar-info b { color: var(--accent); }

/* ── st.metric override ── */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.85rem 1.1rem !important;
}
[data-testid="stMetric"]:hover { border-color: var(--accent); }
[data-testid="stMetricLabel"] {
    font-family: var(--sans) !important;
    font-size: 0.67rem !important;
    color: var(--muted) !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    font-size: 1.05rem !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper: render tile tunggal via HTML (aman, satu div saja) ───────────────
def render_tile(value: str, label: str):
    """Render satu tile metrik sebagai HTML sederhana — aman dari escaping."""
    st.markdown(
        f'<div class="tile"><div class="tv">{value}</div>'
        f'<div class="tl">{label}</div></div>',
        unsafe_allow_html=True,
    )


# ─── Fungsi Perhitungan Inti ───────────────────────────────────────────────────
def hitung_pb(A: float, S: int, N: int):
    """
    Pb = Σ(x=N to S-1) [ (S-1)! / (x! * (S-1-x)!) ] * A^x * (1-A)^(S-1-x)
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
            suku  = binom * (A ** x) * ((1 - A) ** (s1 - x))
            total += suku
        except (OverflowError, ZeroDivisionError):
            return None
    return min(total, 1.0)


def kualitas_layanan(pb: float):
    if pb <= 0.01:
        return "Sangat Baik", "badge-ok"
    elif pb <= 0.05:
        return "Cukup", "badge-mid"
    else:
        return "Buruk", "badge-bad"


def buat_pdf(history: list) -> bytes:
    try:
        from fpdf import FPDF

        def aman(teks: str) -> str:
            pengganti = {
                "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
                "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00d7": "x",
            }
            for k, v in pengganti.items():
                teks = teks.replace(k, v)
            return teks.encode("latin-1", errors="replace").decode("latin-1")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(30, 50, 80)
        pdf.cell(0, 10, aman("Kalkulator Trafik Binomial - Laporan Riwayat"), ln=True)

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 6, aman(f"Dibuat: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"), ln=True)
        pdf.ln(4)

        pdf.set_fill_color(240, 245, 255)
        pdf.set_draw_color(100, 140, 200)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(60, 80, 120)
        pdf.multi_cell(0, 5,
            aman("Rumus: Pb = SIGMA(x=N s/d S-1) [ (S-1)! / (x!(S-1-x)!) ] * A^x * (1-A)^(S-1-x)\n"
                 "Keterangan: A=Erlang/sumber, S=Sumber, N=Server, Pb=Prob. Pemblokiran"),
            border=1, fill=True)
        pdf.ln(6)

        lebar = [28, 18, 18, 18, 32, 28, 40]
        header = ["Waktu", "A", "S", "N", "Pb (%)", "KoL", "Catatan"]
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(30, 50, 80)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(header):
            pdf.cell(lebar[i], 7, aman(h), border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        for idx, r in enumerate(history):
            isi = idx % 2 == 0
            pdf.set_fill_color(248, 250, 255) if isi else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 30, 30)
            pb_pct = f"{r['Pb']*100:.4f}%"
            kol, _ = kualitas_layanan(r['Pb'])
            baris = [
                r.get("Waktu", "")[:16],
                str(r['A']),
                str(r['S']),
                str(r['N']),
                pb_pct,
                kol,
                r.get("Catatan", ""),
            ]
            for i, v in enumerate(baris):
                pdf.cell(lebar[i], 6, aman(v), border=1, fill=isi, align="C" if i != 6 else "L")
            pdf.ln()

        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, aman("Kalkulator Trafik Binomial - Alat Rekayasa Teletrafik"), align="C")

        hasil = pdf.output()
        if isinstance(hasil, (bytes, bytearray)):
            return bytes(hasil)
        return hasil.encode("latin-1")

    except ImportError:
        baris_csv = ["Waktu,A,S,N,Pb,Pb(%),KoL,Catatan"]
        for r in history:
            kol, _ = kualitas_layanan(r['Pb'])
            baris_csv.append(
                f"{r.get('Waktu','')},{r['A']},{r['S']},{r['N']},"
                f"{r['Pb']:.6f},{r['Pb']*100:.4f}%,{kol},{r.get('Catatan','')}"
            )
        return "\n".join(baris_csv).encode("utf-8")


# ─── Inisialisasi State ─────────────────────────────────────────────────────────
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "hasil_terakhir" not in st.session_state:
    st.session_state.hasil_terakhir = None


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">📡 Binomial</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Kalkulator Teletrafik</div>', unsafe_allow_html=True)

    tab = st.radio(
        "Navigasi",
        ["🧮  Kalkulator", "📊  Hasil", "🗂️  Riwayat"],
        label_visibility="collapsed",
    )
    halaman = tab.strip().split("  ", 1)[-1]

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info">
    <b>VARIABEL</b><br>
    <b>A</b> — Erlang per sumber<br>
    <b>S</b> — Total sumber<br>
    <b>N</b> — Jumlah server (saluran)<br>
    <b>Pb</b> — Probabilitas pemblokiran<br>
    <br>
    <b>MODEL</b><br>
    Sumber terbatas (finite source)<br>
    Model binomial dengan asumsi<br>
    pemanggilan ulang (retrial).
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.riwayat:
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        n = len(st.session_state.riwayat)
        st.markdown(
            f'<div class="sidebar-info">📋 <b>{n}</b> catatan tersimpan</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1 — KALKULATOR
# ═══════════════════════════════════════════════════════════════════════════════
if halaman == "Kalkulator":

    st.markdown('<div class="page-title">Kalkulator Trafik Binomial</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Probabilitas pemblokiran sumber terbatas — Model Binomial</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="formula-box">
    <span class="hl">Pb</span>
    &nbsp;=&nbsp; &Sigma; <sub>x=N</sub><sup>S&minus;1</sup>
    &nbsp; <span class="hl2">(S&minus;1)!</span> &nbsp;/&nbsp; [x! &middot; (S&minus;1&minus;x)!]
    &nbsp;&middot;&nbsp; <span class="hl">A</span><sup>x</sup>
    &nbsp;&middot;&nbsp; (1&minus;<span class="hl">A</span>)<sup>(S&minus;1&minus;x)</sup>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Parameter Masukan</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        A = st.number_input(
            "A — Erlang yang Ditawarkan per Sumber",
            min_value=0.001, max_value=0.999,
            value=0.100, step=0.001, format="%.4f",
            help="Intensitas trafik yang ditawarkan oleh setiap sumber individual (0 < A < 1)"
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
            "N — Jumlah Server (Saluran)",
            min_value=1, max_value=499,
            value=3, step=1,
            help="Jumlah server yang tersedia (trunk/sirkuit)"
        )

    if N >= S:
        st.markdown(
            f'<div class="box-warn">&#9888; Nilai N harus lebih kecil dari S. '
            f'Saat ini N={N} &ge; S={S}, sehingga Pb = 0 (tidak ada pemblokiran).</div>',
            unsafe_allow_html=True
        )

    catatan = st.text_input(
        "Catatan (opsional)",
        placeholder="cth. Skenario A — trafik jam sibuk",
        max_chars=80
    )

    st.markdown('<div class="sec-label">Tindakan</div>', unsafe_allow_html=True)

    col_a, col_b, _ = st.columns([1, 1, 5])
    with col_a:
        hitung_btn = st.button("▶  Hitung", use_container_width=True)
    with col_b:
        hapus_btn = st.button("✕  Bersihkan", use_container_width=True)

    if hapus_btn:
        st.session_state.hasil_terakhir = None
        st.rerun()

    if hitung_btn:
        with st.spinner("Menghitung..."):
            pb = hitung_pb(float(A), int(S), int(N))

        if pb is None:
            st.markdown(
                '<div class="box-err">&#9888; Perhitungan gagal — nilai mungkin terlalu besar '
                'untuk kalkulasi faktorial. Coba kurangi nilai S.</div>',
                unsafe_allow_html=True
            )
        else:
            hasil = {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "A": round(float(A), 4),
                "S": int(S),
                "N": int(N),
                "Pb": pb,
                "Catatan": catatan,
            }
            st.session_state.hasil_terakhir = hasil
            st.session_state.riwayat.append(hasil)
            st.success(f"✓ Berhasil dihitung — total {len(st.session_state.riwayat)} catatan tersimpan")

    # ── Pratinjau hasil terakhir ──────────────────────────────────────────────
    if st.session_state.hasil_terakhir:
        r = st.session_state.hasil_terakhir
        kol, badge = kualitas_layanan(r["Pb"])

        st.markdown('<div class="sec-label">Hasil Cepat</div>', unsafe_allow_html=True)

        # Kartu Pb utama
        catatan_html = (
            f"<div class='result-sub'><i>{r['Catatan']}</i></div>"
            if r['Catatan'] else ""
        )
        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-big">{r["Pb"]*100:.4f}%</div>'
            f'<div class="result-label">Probabilitas Pemblokiran (Pb)</div>'
            f'{catatan_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── FIX: tile baris bawah pakai st.columns + st.metric ──────────────
        # Ini menggantikan blok HTML tile-row yang bermasalah
        tc1, tc2, tc3, tc4 = st.columns(4)
        tc1.metric("A (Erlang/Sumber)", r["A"])
        tc2.metric("S (Sumber)", r["S"])
        tc3.metric("N (Server)", r["N"])
        with tc4:
            st.metric("Kualitas Layanan", kol)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2 — HASIL
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "Hasil":

    st.markdown('<div class="page-title">Hasil Perhitungan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Rincian lengkap dari komputasi terakhir</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.hasil_terakhir:
        st.markdown(
            '<div class="box-info">&#8505; Belum ada perhitungan. '
            'Buka tab <b>Kalkulator</b> dan jalankan perhitungan terlebih dahulu.</div>',
            unsafe_allow_html=True
        )
    else:
        r = st.session_state.hasil_terakhir
        pb = r["Pb"]
        kol, badge = kualitas_layanan(pb)
        trafik_total   = r['A'] * r['S']
        beban_diterima = trafik_total * (1 - pb)
        trafik_blokir  = trafik_total * pb

        # ── Hasil utama ──
        st.markdown('<div class="sec-label">Hasil Utama</div>', unsafe_allow_html=True)
        catatan_html = (
            f"<div class='result-sub'><i>Catatan: {r['Catatan']}</i></div>"
            if r['Catatan'] else ""
        )
        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-big">{pb*100:.6f}%</div>'
            f'<div class="result-label">Probabilitas Pemblokiran (Pb)</div>'
            f'<div style="margin-top:0.6rem;">'
            f'<span class="badge {badge}">{kol}</span>'
            f'&nbsp;<span style="font-size:0.75rem;color:var(--muted);font-family:var(--mono);">Kualitas Layanan</span>'
            f'</div>'
            f'<div class="result-sub">Desimal: <code style="color:var(--accent);">{pb:.10f}</code></div>'
            f'<div class="result-sub">Waktu: <code style="font-size:0.78rem;color:var(--muted);">{r["Waktu"]}</code></div>'
            f'{catatan_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── FIX: Parameter masukan — st.columns + st.metric ─────────────────
        st.markdown('<div class="sec-label">Parameter Masukan</div>', unsafe_allow_html=True)
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("A — Erlang/Sumber", r['A'])
        pc2.metric("S — Jumlah Sumber", r['S'])
        pc3.metric("N — Jumlah Server", r['N'])
        pc4.metric("S - N (Sumber Berlebih)", r['S'] - r['N'])

        # ── FIX: Metrik trafik turunan — st.columns + st.metric ─────────────
        st.markdown('<div class="sec-label">Metrik Trafik Turunan</div>', unsafe_allow_html=True)
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Total Ditawarkan (Erl)", f"{trafik_total:.4f}")
        mc2.metric("Beban Diterima (Erl)",   f"{beban_diterima:.4f}")
        mc3.metric("Trafik Terblokir (Erl)", f"{trafik_blokir:.4f}")
        mc4.metric("Tingkat Keberhasilan",   f"{(1-pb)*100:.4f}%")

        # ── Grafik distribusi suku ──
        st.markdown('<div class="sec-label">Grafik Distribusi Suku Penjumlahan</div>', unsafe_allow_html=True)
        A_v, S_v, N_v = r['A'], r['S'], r['N']
        s1 = S_v - 1
        data_suku = []
        for x in range(0, S_v):
            try:
                binom = math.factorial(s1) / (math.factorial(x) * math.factorial(s1 - x))
                suku  = binom * (A_v ** x) * ((1 - A_v) ** (s1 - x))
                data_suku.append({
                    "x (Sumber Aktif)": x,
                    "Probabilitas": round(suku, 8),
                    "Zona": "Pemblokiran (x >= N)" if x >= N_v else "Normal (x < N)"
                })
            except Exception:
                pass

        if data_suku:
            df_suku = pd.DataFrame(data_suku)
            df_plot = df_suku.set_index("x (Sumber Aktif)")[["Probabilitas"]]
            st.area_chart(df_plot, height=220, use_container_width=True)

            st.markdown('<div class="sec-label">Kontribusi Zona Pemblokiran (x &ge; N)</div>', unsafe_allow_html=True)
            df_blok = df_suku[df_suku["x (Sumber Aktif)"] >= N_v].copy()
            if not df_blok.empty:
                df_blok["Kumulatif Pb"] = df_blok["Probabilitas"].cumsum()
                df_blok2 = df_blok.set_index("x (Sumber Aktif)")[["Probabilitas", "Kumulatif Pb"]]
                st.line_chart(df_blok2, height=200, use_container_width=True)
                st.markdown(
                    f'<div class="box-info">Zona pemblokiran mencakup <b>{len(df_blok)}</b> suku '
                    f'(x = {N_v} hingga {S_v-1}). Total Pb = <b>{pb*100:.4f}%</b></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="box-info">Tidak ada suku dalam zona pemblokiran (N &ge; S).</div>',
                    unsafe_allow_html=True
                )

        # ── Analisis sensitivitas ──
        st.markdown('<div class="sec-label">Analisis Sensitivitas — Tambah 1 Server</div>', unsafe_allow_html=True)
        pb_plus1 = hitung_pb(r['A'], r['S'], r['N'] + 1)
        if pb_plus1 is not None and r['N'] + 1 < r['S']:
            delta = pb - pb_plus1
            kol2, badge2 = kualitas_layanan(pb_plus1)
            st.markdown(
                f'<div class="box-info">'
                f'Menambah 1 server (N &rarr; <b>{r["N"]+1}</b>) akan menurunkan Pb dari '
                f'<b>{pb*100:.4f}%</b> menjadi <b>{pb_plus1*100:.4f}%</b>'
                f'&nbsp;(&Delta; = &minus;{delta*100:.4f} pp)&nbsp; '
                f'<span class="badge {badge2}">{kol2}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Grafik Pb vs jumlah server
            st.markdown('<div class="sec-label">Grafik Pb terhadap Jumlah Server (N)</div>', unsafe_allow_html=True)
            data_server = []
            for n_i in range(1, min(r['S'], 30)):
                pb_i = hitung_pb(r['A'], r['S'], n_i)
                if pb_i is not None:
                    data_server.append({"N (Server)": n_i, "Pb (%)": round(pb_i * 100, 6)})
            if data_server:
                df_server = pd.DataFrame(data_server).set_index("N (Server)")
                st.line_chart(df_server, height=220, use_container_width=True)
                st.markdown(
                    '<div class="box-info">Grafik menunjukkan hubungan antara jumlah server dan probabilitas '
                    'pemblokiran dengan nilai A dan S tetap. Semakin banyak server, semakin kecil Pb.</div>',
                    unsafe_allow_html=True
                )

        # ── Penjelasan formula ──
        with st.expander("📐 Penjelasan Rumus Langkah demi Langkah"):
            st.markdown(f"""
**Rumus Pemblokiran Binomial:**

```
Pb = Σ(x = N sampai S-1)  [ (S-1)! / (x! · (S-1-x)!) ]  ·  A^x  ·  (1-A)^(S-1-x)
```

**Dengan nilai Anda** — A = {r['A']}, S = {r['S']}, N = {r['N']}:

- Penjumlahan berjalan dari x = **{r['N']}** sampai x = **{r['S']-1}**
- Total suku yang dievaluasi: **{r['S'] - r['N']}**
- S-1 = **{r['S']-1}**, (1-A) = **{round(1-r['A'], 4)}**

Setiap suku merepresentasikan probabilitas bahwa tepat *x* dari *S-1* sumber
sedang aktif secara bersamaan, dibobot dengan koefisien binomial.
Jumlah total memberikan probabilitas bahwa semua N server sedang sibuk
ketika panggilan baru tiba.

| Simbol | Keterangan | Nilai |
|--------|-----------|-------|
| A | Erlang yang ditawarkan per sumber | {r['A']} |
| S | Jumlah sumber | {r['S']} |
| N | Jumlah server | {r['N']} |
| Pb | Probabilitas pemblokiran | {pb:.8f} |
""")


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3 — RIWAYAT
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "Riwayat":

    st.markdown('<div class="page-title">Riwayat Perhitungan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Semua komputasi dalam sesi ini</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.riwayat:
        st.markdown(
            '<div class="box-info">&#8505; Belum ada riwayat. '
            'Jalankan perhitungan di tab <b>Kalkulator</b>.</div>',
            unsafe_allow_html=True
        )
    else:
        n = len(st.session_state.riwayat)
        semua_pb = [r["Pb"] for r in st.session_state.riwayat]

        # ── FIX: Ringkasan statistik — st.columns + st.metric ───────────────
        st.markdown('<div class="sec-label">Ringkasan Sesi</div>', unsafe_allow_html=True)
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("Total Catatan", n)
        rc2.metric("Pb Minimum",  f"{min(semua_pb)*100:.4f}%")
        rc3.metric("Pb Maksimum", f"{max(semua_pb)*100:.4f}%")
        rc4.metric("Pb Rata-rata", f"{sum(semua_pb)/n*100:.4f}%")

        # Tabel catatan
        st.markdown('<div class="sec-label">Tabel Catatan</div>', unsafe_allow_html=True)
        baris_tabel = []
        for i, r in enumerate(reversed(st.session_state.riwayat), 1):
            kol, _ = kualitas_layanan(r["Pb"])
            baris_tabel.append({
                "#": n - i + 1,
                "Waktu": r["Waktu"],
                "A": r["A"],
                "S": r["S"],
                "N": r["N"],
                "Pb (desimal)": f"{r['Pb']:.8f}",
                "Pb (%)": f"{r['Pb']*100:.4f}%",
                "Kualitas": kol,
                "Catatan": r.get("Catatan", ""),
            })

        df = pd.DataFrame(baris_tabel)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Grafik tren
        st.markdown('<div class="sec-label">Tren Probabilitas Pemblokiran</div>', unsafe_allow_html=True)
        df_tren = pd.DataFrame({
            "Catatan ke-": list(range(1, n + 1)),
            "Pb (%)": [r["Pb"] * 100 for r in st.session_state.riwayat],
        }).set_index("Catatan ke-")
        st.line_chart(df_tren, height=230, use_container_width=True)

        # Grafik perbandingan parameter
        st.markdown('<div class="sec-label">Perbandingan Parameter (A, S, N)</div>', unsafe_allow_html=True)
        df_param = pd.DataFrame({
            "Catatan ke-": list(range(1, n + 1)),
            "A (x100)": [r["A"] * 100 for r in st.session_state.riwayat],
            "S": [r["S"] for r in st.session_state.riwayat],
            "N": [r["N"] for r in st.session_state.riwayat],
        }).set_index("Catatan ke-")
        st.line_chart(df_param, height=200, use_container_width=True)

        # Ekspor
        st.markdown('<div class="sec-label">Ekspor Data</div>', unsafe_allow_html=True)
        col_p, col_c, col_h, _ = st.columns([1.2, 1.2, 1, 3])

        with col_p:
            try:
                from fpdf import FPDF  # noqa
                pdf_bytes = buat_pdf(st.session_state.riwayat)
                file_ext = "pdf"
                mime_type = "application/pdf"
                label_btn = "⬇  Unduh PDF"
            except ImportError:
                pdf_bytes = buat_pdf(st.session_state.riwayat)
                file_ext = "txt"
                mime_type = "text/plain"
                label_btn = "⬇  Unduh TXT"

            st.download_button(
                label=label_btn,
                data=pdf_bytes,
                file_name=f"riwayat_binomial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                mime=mime_type,
                use_container_width=True,
            )

        with col_c:
            baris_csv = ["Waktu,A,S,N,Pb,Pb(%),Kualitas,Catatan"]
            for r in st.session_state.riwayat:
                kol, _ = kualitas_layanan(r["Pb"])
                baris_csv.append(
                    f"{r['Waktu']},{r['A']},{r['S']},{r['N']},"
                    f"{r['Pb']:.8f},{r['Pb']*100:.4f}%,{kol},{r.get('Catatan','')}"
                )
            csv_data = "\n".join(baris_csv)
            st.download_button(
                label="⬇  Unduh CSV",
                data=csv_data.encode("utf-8"),
                file_name=f"riwayat_binomial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col_h:
            if st.button("🗑  Hapus Semua", use_container_width=True):
                st.session_state.riwayat = []
                st.session_state.hasil_terakhir = None
                st.rerun()
