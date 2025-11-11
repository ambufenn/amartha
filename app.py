import streamlit as st
import pandas as pd
import os

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="SERENADE - Amartha Hackathon",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Path ke folder app.py (aman di lokal & cloud) ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Fungsi Load Data ---
@st.cache_data
def load_data():
    data_dir = os.path.join(APP_DIR, "data")
    customers = pd.read_csv(os.path.join(data_dir, "mock_customers.csv"))
    loans = pd.read_csv(os.path.join(data_dir, "mock_loans.csv"))
    repayments = pd.read_csv(os.path.join(data_dir, "mock_repayments.csv"))
    return customers, loans, repayments

# --- Load data ---
try:
    customers, loans, repayments = load_data()
except Exception as e:
    st.error(f"❌ Gagal memuat data: {e}")
    st.stop()

# --- Sidebar Navigasi ---
st.sidebar.title("🧭 SINAR")
role = st.sidebar.radio("Pilih Mode", ["Mitra (Peminjam)", "Amartha (Admin)"])

# ========================================
# HALAMAN: MITRA
# ========================================
if role == "Mitra (Peminjam)":
    st.title("🌸 Halo, Mitra Amartha!")
    st.markdown("SINAR siap membantu Ibu dengan edukasi, konsultasi, dan saluran resmi saat ada kendala.")

    # Chatbot sederhana
    st.subheader("💬 Tanya Ayu (Asisten Virtual)")
    user_msg = st.text_input("Apa yang ingin Ibu tanyakan?")
    if user_msg:
        msg_lower = user_msg.lower()
        if "telat" in msg_lower or "lambat" in msg_lower:
            response = "Tenang, Bu. Jika Ibu telat karena kendala, segera ajukan 'Lapor Kendala' di bawah. Selama ditinjau, Ibu tidak akan dihubungi penagih."
        elif "perpanjang" in msg_lower or "keringanan" in msg_lower:
            response = "Ibu bisa ajukan perpanjangan lewat 'Lapor Kendala'. Unggah foto bukti (misal: sawah gagal panen), lalu tim Amartha akan bantu."
        else:
            response = "Terima kasih, Bu! 💕 Jika ada kendala, jangan sungkan ajukan 'Lapor Kendala'."
        st.info(response)

    # Fitur Lapor Kendala
    st.markdown("---")
    st.subheader("📌 Lapor Kendala – Ajukan Keringanan")
    with st.form("lapor_form"):
        jenis = st.selectbox("Jenis Kendala", [
            "Gagal panen / gagal usaha",
            "Bencana alam",
            "Sakit atau kecelakaan",
            "Usaha sepi",
            "Lainnya"
        ])
        keterangan = st.text_area("Ceritakan kondisi Ibu (opsional):")
        bukti = st.file_uploader("Unggah foto bukti:", type=["jpg", "png"])
        submit = st.form_submit_button("Ajukan Permohonan")

    if submit:
        st.success("✅ Permohonan Ibu telah diajukan!\n\n"
                   "Sawah Ibu betul terdeteksi Kering/gagal panen, maka Tim Amartha akan segera meninjau. **Selama proses ini, Ibu tidak akan dihubungi penagih.**")
        if bukti:
            st.image(bukti, caption="Bukti yang diunggah", use_container_width=True)

# ========================================
# HALAMAN: AMARTHA (ADMIN)
# ========================================
else:
    st.title("🛡️ Dashboard SINAR – Analitik Risiko & Responsif")
    st.markdown("Mendeteksi risiko dini & merespons kendala mitra secara proaktif.")

    # Gabungkan data — pastikan pakai 'loans' (dengan 's')!
    try:
        merged = loans.merge(customers, on="mitra_id", how="left")
        # Tambahkan kolom risiko berdasarkan status pinjaman
        def tentukan_risiko(status):
            if status == "lancar":
                return "Rendah"
            elif status in ["terlambat", "belum_bayar"]:
                return "Sedang"
            else:
                return "Tinggi"
        merged["risiko"] = merged["status"].apply(tentukan_risiko)
    except KeyError as e:
        st.error(f"❌ Kolom tidak ditemukan di data: {e}")
        st.write("Pastikan file CSV memiliki kolom: `mitra_id`, `status`")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error saat menggabung data: {e}")
        st.stop()

    # Tampilkan mitra berisiko
    st.subheader("🚨 Mitra Perlu Perhatian")
    high_risk = merged[merged["risiko"] != "Rendah"]
    if not high_risk.empty:
        st.dataframe(
            high_risk[["nama", "desa", "jumlah_pinjaman", "status", "risiko"]],
            hide_index=True
        )
    else:
        st.info("Tidak ada mitra berisiko tinggi saat ini.")

    # Grafik cohort mock
    st.subheader("📊 Performa Kelompok (Cohort)")
    st.bar_chart({
        "Kelompok A": 96,
        "Kelompok B": 89,
        "Kelompok C": 93
    }, y_label="Tingkat Kelancaran (%)", color="#4CAF50")

    # Permohonan kendala (mock)
    st.subheader("📥 Permohonan Kendala Terbaru")
    st.warning("Contoh permohonan:\n- Ibu Siti (Kelompok A): Gagal panen → perlu verifikasi\n- Ibu Rina (Kelompok B): Sakit → ajukan penundaan")
