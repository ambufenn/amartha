import streamlit as st
import pandas as pd
import os

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="SINAR - Amartha Hackathon",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Sidebar Navigasi ---
st.sidebar.title("🧭 Navigasi SINAR")
role = st.sidebar.radio("Pilih Mode", ["Mitra (Peminjam)", "Amartha (Admin)"])

# --- Load Data Mock ---
@st.cache_data
def load_data():
    customers = pd.read_csv("data/mock_customers.csv")
    loans = pd.read_csv("data/mock_loans.csv")
    repayments = pd.read_csv("data/mock_repayments.csv")
    return customers, loans, repayments

customers, loans, repayments = load_data()

# ========================================
# HALAMAN 1: MITRA (PEMINJAM)
# ========================================
if role == "Mitra (Peminjam)":
    st.title("🌸 Selamat Datang, Mitra Amartha!")
    st.markdown("SINAR hadir untuk mendukung Ibu dengan **edukasi, konsultasi, dan saluran resmi** saat mengalami kendala.")
    
    # --- Chatbot Mock (tanpa AI dulu) ---
    st.subheader("💬 Ayu – Asisten Literasi & Dukungan")
    user_msg = st.text_input("Tulis pertanyaan Ibu di sini (contoh: 'Bagaimana kalau telat bayar?'):")
    
    if user_msg:
        user_lower = user_msg.lower()
        if "telat" in user_lower or "lambat" in user_lower:
            response = "Tenang, Bu. Jika Ibu telat bayar karena kendala, segera ajukan 'Lapor Kendala' di bawah. Selama proses ditinjau, Ibu tidak akan dihubungi penagih."
        elif "perpanjang" in user_lower or "keringanan" in user_lower:
            response = "Ibu bisa ajukan perpanjangan atau keringanan lewat menu 'Lapor Kendala'. Unggah foto bukti kendala (misal: sawah gagal panen), lalu tim Amartha akan bantu."
        elif "cara bayar" in user_lower:
            response = "Ibu bisa bayar langsung ke agen lapangan saat kunjungan mingguan, atau lewat transfer ke rekening yang tercantum di aplikasi Amartha."
        else:
            response = "Terima kasih sudah bertanya, Bu! 💕 Tim Amartha selalu siap mendukung Ibu. Kalau ada kendala usaha atau keluarga, jangan sungkan ajukan 'Lapor Kendala'."
        st.info(response)

    # --- Fitur Lapor Kendala ---
    st.markdown("---")
    st.subheader("📌 Lapor Kendala – Ajukan Keringanan Resmi")
    with st.form("lapor_kendala"):
        jenis = st.selectbox("Jenis Kendala", [
            "Gagal panen / gagal usaha",
            "Bencana alam (banjir, kekeringan)",
            "Sakit atau kecelakaan keluarga",
            "Usaha sepi / omzet turun drastis",
            "Lainnya"
        ])
        keterangan = st.text_area("Ceritakan kondisi Ibu (opsional):")
        bukti = st.file_uploader("Unggah foto bukti (sawah, toko, surat dokter, dll):", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Ajukan Permohonan")

    if submit:
        st.success("✅ Permohonan Ibu telah diajukan!\n\n"
                   "Tim Amartha akan segera meninjau. **Selama proses ini, Ibu tidak akan dihubungi penagih.**\n\n"
                   "Terima kasih atas kejujuran dan komunikasi Ibu. 💪")
        if bukti:
            st.image(bukti, caption="Bukti yang diunggah", use_container_width=True)

# ========================================
# HALAMAN 2: AMARTHA (ADMIN)
# ========================================
else:
    st.title("🛡️ Dashboard SINAR – Analitik Risiko & Responsif")
    st.markdown("Dashboard ini membantu tim Amartha **mendeteksi dini risiko** dan **merespons kendala mitra**.")

    # Gabungkan data
    merged = loans.merge(customers, on="mitra_id", how="left")
    merged["risiko"] = merged["status"].apply(lambda x: "Rendah" if x == "lancar" else "Sedang" if x == "terlambat" else "Tinggi")

    # Tabel mitra berisiko
    st.subheader("🚨 Mitra Perlu Perhatian")
    high_risk = merged[merged["risiko"] != "Rendah"]
    if not high_risk.empty:
        st.dataframe(high_risk[["nama", "desa", "jumlah_pinjaman", "status", "risiko"]], hide_index=True)
    else:
        st.info("Tidak ada mitra berisiko tinggi saat ini.")

    # Grafik cohort mock
    st.subheader("📊 Performa Kelompok (Cohort)")
    st.bar_chart({"Kelompok A": 98, "Kelompok B": 85, "Kelompok C": 92}, 
                 y_label="Tingkat Kelancaran (%)", 
                 color="#4CAF50")

    # Daftar permohonan kendala (mock)
    st.subheader("📥 Permohonan Kendala Terbaru")
    st.warning("Fitur ini akan menampilkan daftar permohonan dari mitra saat terintegrasi dengan database.")
    st.markdown("Contoh permohonan:\n- **Ibu Siti** (Kelompok A): Gagal panen → perlu verifikasi lapangan\n- **Ibu Rina** (Kelompok B): Sakit anak → ajukan penundaan 14 hari")
