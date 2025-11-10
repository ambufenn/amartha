import streamlit as st
import pandas as pd
import os

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="SINAR - Amartha Hackathon",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Dapatkan path absolut ke folder app.py ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Load Data dengan Error Handling ---
@st.cache_resource
def load_data():
    try:
        data_dir = os.path.join(APP_DIR, "data")
        customers = pd.read_csv(os.path.join(data_dir, "mock_customers.csv"))
        loans = pd.read_csv(os.path.join(data_dir, "mock_loans.csv"))
        repayments = pd.read_csv(os.path.join(data_dir, "mock_repayments.csv"))
        return customers, loans, repayments
    except Exception as e:
        st.error(f"⚠️ Gagal memuat data: {str(e)}")
        # Kembalikan data dummy jika gagal
        customers = pd.DataFrame({"mitra_id": ["M001"], "nama": ["Ibu Contoh"], "desa": ["Desa Demo"], "kelompok": ["Kelompok X"]})
        loans = pd.DataFrame({"loan_id": ["L001"], "mitra_id": ["M001"], "jumlah_pinjaman": [1000000], "status": ["lancar"]})
        repayments = pd.DataFrame({"repayment_id": ["R001"], "loan_id": ["L001"], "status": ["lunas"]})
        return customers, loans, repayments

# --- Sidebar ---
st.sidebar.title("🧭 Navigasi SINAR")
role = st.sidebar.radio("Pilih Mode", ["Mitra (Peminjam)", "Amartha (Admin)"])

# --- Load Data ---
customers, loans, repayments = load_data()

# ========================================
# HALAMAN: MITRA
# ========================================
if role == "Mitra (Peminjam)":
    st.title("🌸 Selamat Datang, Mitra Amartha!")
    st.markdown("SINAR hadir untuk mendukung Ibu dengan edukasi, konsultasi, dan saluran resmi saat mengalami kendala.")

    user_msg = st.text_input("Tulis pertanyaan Ibu di sini:")
    if user_msg:
        response = "Terima kasih, Bu! Jika Ibu mengalami kendala, jangan sungkan ajukan 'Lapor Kendala' di bawah. 💕"
        st.info(response)

    st.markdown("---")
    st.subheader("📌 Lapor Kendala – Ajukan Keringanan Resmi")
    with st.form("lapor_kendala"):
        jenis = st.selectbox("Jenis Kendala", ["Gagal panen", "Sakit", "Usaha sepi", "Lainnya"])
        bukti = st.file_uploader("Unggah foto bukti:", type=["jpg", "png"])
        submit = st.form_submit_button("Ajukan")
    if submit:
        st.success("✅ Permohonan Ibu telah diajukan! Tim Amartha akan segera meninjau.")

# ========================================
# HALAMAN: AMARTHA (ADMIN)
# ========================================
else:
    st.title("🛡️ Dashboard SINAR – Analitik Risiko & Responsif")
    st.markdown("Dashboard ini membantu tim Amartha mendeteksi dini risiko dan merespons kendala mitra.")

    # Cek apakah kolom yang dibutuhkan ada
    try:
        if "mitra_id" not in loans.columns or "mitra_id" not in customers.columns:
            st.warning("⚠️ Kolom 'mitra_id' tidak ditemukan di data. Gunakan data dummy.")
            loans = pd.DataFrame({"mitra_id": ["M001"], "jumlah_pinjaman": [1000000], "status": ["lancar"]})
            customers = pd.DataFrame({"mitra_id": ["M001"], "nama": ["Ibu Demo"], "desa": ["Desa X"], "kelompok": ["K1"]})

        merged = loans.merge(customers, on="mitra_id", how="left")
        merged["risiko"] = merged["status"].apply(
            lambda x: "Rendah" if x == "lancar" else "Sedang" if x in ["terlambat", "belum_bayar"] else "Tinggi"
        )

        st.subheader("🚨 Mitra Perlu Perhatian")
        high_risk = merged[merged["risiko"] != "Rendah"]
        if not high_risk.empty:
            st.dataframe(high_risk[["nama", "desa", "jumlah_pinjaman", "status", "risiko"]], hide_index=True)
        else:
            st.info("Tidak ada mitra berisiko tinggi.")

        st.subheader("📊 Performa Kelompok (Cohort)")
        st.bar_chart({"Kelompok K1": 95, "Kelompok K2": 88}, y_label="Kelancaran (%)")

    except Exception as e:
        st.error(f"❌ Error saat memproses data dashboard: {str(e)}")
        st.write("Pastikan file CSV memiliki kolom: `mitra_id`, `status`, `nama`, `desa`, `jumlah_pinjaman`.")
