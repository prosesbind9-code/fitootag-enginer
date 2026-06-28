import streamlit as st
import io
import re

# --- 1. KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="FitooTag - Pencari Tag Nomor HP", 
    page_icon="🔍", 
    layout="centered"
)

# Desain Antarmuka Premium (Clean Blue & Slate Theme)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #1e293b; }
    .stButton>button {
        background-image: linear-gradient(to right, #2563eb , #1d4ed8);
        color: white; border-radius: 8px; border: none;
        padding: 10px 20px; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    h1, h2, h3 { color: #1e40af !important; font-weight: bold; }
    .tag-container {
        background-color: #ffffff;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .info-box {
        background-color: #eff6ff;
        padding: 15px;
        border-radius: 8px;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SIMULASI (IN-MEMORY SESSION STATE) ---
if 'database_tag' not in st.session_state:
    st.session_state['database_tag'] = {
        "08123456789": ["Fitzz Developer", "Fitoo VIP Oprek", "Fitoo Teman Sekelas"],
        "08555555555": ["Penipu Toko Online", "Spam Penawaran Pinjol", "Jangan Diangkat"],
        "08999888777": ["Budi Setiawan", "Kurir Paket J&T"]
    }

st.title("🔍 FitooTag - GetContact Clone")
st.write("Cari nama/tag dari nomor telepon asing berbasis database kontribusi komunitas.")
st.markdown("---")

# Pemisahan Fitur menggunakan Tab Menu
tab1, tab2 = st.tabs(["🔎 Cari Nomor HP", "📥 Kontribusi Data (Crowdsourcing)"])

# --- TAB 1: LOGIKA PENCARIAN ---
with tab1:
    st.subheader("Masukkan Nomor Telepon")
    search_num = st.text_input("Contoh: 08123456789", key="search_input").strip()
    
    if st.button("Periksa Nomor"):
        if not search_num:
            st.warning("Silakan masukkan nomor HP terlebih dahulu!")
        else:
            # Normalisasi input nomor (Hanya ambil angka saja)
            search_num_clean = re.sub(r'\D', '', search_num)
            if search_num_clean.startswith("62"):
                search_num_clean = "0" + search_num_clean[2:]
                
            if search_num_clean in st.session_state['database_tag']:
                tags = st.session_state['database_tag'][search_num_clean]
                st.success(f"Ditemukan {len(tags)} tag untuk nomor {search_num}")
                for tag in tags:
                    st.markdown(f'<div class="tag-container"><b>👤 {tag}</b></div>', unsafe_allow_html=True)
            else:
                st.info("Nomor tidak ditemukan di database database lokal kami.")

# --- TAB 2: LOGIKA PENAMBAHAN DATA (CROWDSOURCING SIMULATION) ---
with tab2:
    st.markdown("""
    <div class="info-box">
        <b>💡 Konsep Crowdsourcing:</b> Pengguna saling berbagi daftar kontak. Kamu bisa mensimulasikannya dengan memasukkan nama manual atau upload file teks secara massal.
    </div>
    """, unsafe_allow_html=True)
    
    menu_opsi = st.radio("Metode Kontribusi", ["Input Manual Satu Per Satu", "Upload Massal via File Teks (.txt)"])
    
    if menu_opsi == "Input Manual Satu Per Satu":
        input_num = st.text_input("Nomor HP Target")
        input_tag = st.text_input("Nama/Tag Kontak")
        
        if st.button("Simpan Tag Ke Database"):
            if input_num and input_tag:
                num_clean = re.sub(r'\D', '', input_num)
                if num_clean.startswith("62"):
                    num_clean = "0" + num_clean[2:]
                
                # Masukkan ke dalam database sementara
                if num_clean in st.session_state['database_tag']:
                    if input_tag not in st.session_state['database_tag'][num_clean]:
                        st.session_state['database_tag'][num_clean].append(input_tag)
                else:
                    st.session_state['database_tag'][num_clean] = [input_tag]
                st.success(f"Sukses menambahkan tag '{input_tag}'!")
            else:
                st.error("Mohon isi data nomor dan tag dengan lengkap!")
                
    elif menu_opsi == "Upload Massal via File Teks (.txt)":
        st.write("Format isi file per baris harus berupa: `NomorHP,NamaTag`")
        st.caption("Contoh: 08122223333,Budi Target")
        uploaded_file = st.file_uploader("Pilih file teks", type=["txt"])
        
        if uploaded_file is not None:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            lines = stringio.readlines()
            count = 0
            for line in lines:
                if "," in line:
                    parts = line.strip().split(",", 1)
                    num_part = re.sub(r'\D', '', parts[0])
                    if num_part.startswith("62"):
                        num_part = "0" + num_part[2:]
                    tag_part = parts[1].strip()
                    
                    if num_part and tag_part:
                        if num_part in st.session_state['database_tag']:
                            if tag_part not in st.session_state['database_tag'][num_part]:
                                st.session_state['database_tag'][num_part].append(tag_part)
                        else:
                            st.session_state['database_tag'][num_part] = [tag_part]
                        count += 1
            st.success(f"Berhasil mengimpor {count} data kontak baru ke database!")

st.markdown("---")
st.caption("FitooTag Engine v1.0 | Platform © 2026")
