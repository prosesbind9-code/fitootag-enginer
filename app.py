import streamlit as st
import io
import re

# --- 1. SETTING HALAMAN ---
st.set_page_config(
    page_title="FitooTag Fix-Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Custom CSS biar tampilan tetep cakep
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #1e293b; }
    .stButton>button {
        background-image: linear-gradient(to right, #2563eb , #1d4ed8);
        color: white; border-radius: 8px; border: none; font-weight: bold; width: 100%;
    }
    .tag-container {
        background-color: #ffffff; padding: 12px 16px; border-radius: 8px;
        border-left: 4px solid #3b82f6; margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INSTANS IAS DATABASE (ANTI RISIKO ERROR KEY) ---
if 'database_tag' not in st.session_state:
    st.session_state['database_tag'] = {
        "08123456789": ["Fitzz Developer", "Fitoo VIP Oprek"],
        "08555555555": ["Spam Penawaran Pinjol"]
    }

st.title("🔍 FitooTag - Engine Fix Version")
st.write("Cari nama/tag dari nomor telepon asing berbasis database kontribusi komunitas.")
st.markdown("---")

tab1, tab2 = st.tabs(["🔎 Cari Nomor HP", "📥 Kontribusi Data (Crowdsourcing)"])

# --- TAB 1: LOGIKA PENCARIAN ---
with tab1:
    st.subheader("Masukkan Nomor Telepon")
    search_num = st.text_input("Contoh: 08123456789", key="user_search_input").strip()
    
    if st.button("Periksa Nomor"):
        if not search_num:
            st.warning("Silakan masukkan nomor HP terlebih dahulu!")
        else:
            # Ambil hanya angka
            search_num_clean = re.sub(r'\D', '', search_num)
            if search_num_clean.startswith("62"):
                search_num_clean = "0" + search_num_clean[2:]
                
            if search_num_clean in st.session_state['database_tag']:
                tags = st.session_state['database_tag'][search_num_clean]
                st.success(f"Ditemukan {len(tags)} tag")
                for tag in tags:
                    st.markdown(f'<div class="tag-container"><b>👤 {tag}</b></div>', unsafe_allow_html=True)
            else:
                st.info("Nomor tidak ditemukan di database.")

# --- TAB 2: LOGIKA PARSER FILE (ANTI EROR MERAH) ---
with tab2:
    st.write("Unggah file kontak (.txt atau .vcf)")
    uploaded_file = st.file_uploader("Pilih file kamu", type=["txt", "vcf"])
    
    if uploaded_file is not None:
        try:
            # Membaca isi file dengan aman
            file_bytes = uploaded_file.getvalue()
            file_contents = file_bytes.decode("utf-8", errors="ignore")
            count = 0
            
            # CEK JIKA FILE ADALAH VCF
            if uploaded_file.name.lower().endswith('.vcf'):
                # Pecah file berdasarkan baris teks untuk menghindari crash memory
                lines = file_contents.splitlines()
                current_fn = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("FN:"):
                        current_fn = line.replace("FN:", "").strip()
                    elif line.startswith("TEL;") or line.startswith("TEL:"):
                        # Ambil angka setelah tanda titik dua (:)
                        if ":" in line:
                            raw_phone = line.split(":", 1)[1]
                            phone_clean = re.sub(r'\D', '', raw_phone)
                            
                            if phone_clean.startswith("62"):
                                phone_clean = "0" + phone_clean[2:]
                                
                            if phone_clean and current_fn:
                                if phone_clean in st.session_state['database_tag']:
                                    if current_fn not in st.session_state['database_tag'][phone_clean]:
                                        st.session_state['database_tag'][phone_clean].append(current_fn)
                                else:
                                    st.session_state['database_tag'][phone_clean] = [current_fn]
                                count += 1
                                
            # CEK JIKA FILE ADALAH TXT
            elif uploaded_file.name.lower().endswith('.txt'):
                lines = file_contents.splitlines()
                for line in lines:
                    if "," in line:
                        parts = line.strip().split(",", 1)
                        phone_clean = re.sub(r'\D', '', parts[0])
                        if phone_clean.startswith("62"):
                            phone_clean = "0" + phone_clean[2:]
                        tag_name = parts[1].strip()
                        
                        if phone_clean and tag_name:
                            if phone_clean in st.session_state['database_tag']:
                                if tag_name not in st.session_state['database_tag'][phone_clean]:
                                    st.session_state['database_tag'][phone_clean].append(tag_name)
                            else:
                                st.session_state['database_tag'][phone_clean] = [tag_name]
                            count += 1
            
            if count > 0:
                st.success(f"🚀 Sukses besar! Berhasil memasukkan {count} data ke database.")
            else:
                st.warning("File berhasil dibaca, tapi tidak ada format nomor & nama yang cocok ditemukan.")
                
        except Exception as e:
            st.error(f"Sistem gagal memproses file ini karena: {e}")
