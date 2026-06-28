import streamlit as st
import io
import re

st.set_page_config(
    page_title="FitooTag Pro - VCF Supported", 
    page_icon="🔍", 
    layout="centered"
)

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #1e293b; }
    .stButton>button {
        background-image: linear-gradient(to right, #2563eb , #1d4ed8);
        color: white; border-radius: 8px; border: none;
        padding: 10px 20px; font-weight: bold; width: 100%;
    }
    .tag-container {
        background-color: #ffffff; padding: 12px 16px; border-radius: 8px;
        border-left: 4px solid #3b82f6; margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .info-box {
        background-color: #eff6ff; padding: 15px; border-radius: 8px;
        color: #1e40af; border: 1px solid #bfdbfe; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'database_tag' not in st.session_state:
    st.session_state['database_tag'] = {
        "08123456789": ["Fitzz Developer", "Fitoo VIP Oprek"],
        "08555555555": ["Spam Penawaran Pinjol"]
    }

st.title("🔍 FitooTag Pro - Multi-Format Engine")
st.write("Cari nama/tag dari nomor telepon asing berbasis database kontribusi komunitas.")
st.markdown("---")

tab1, tab2 = st.tabs(["🔎 Cari Nomor HP", "📥 Kontribusi Data (Crowdsourcing)"])

with tab1:
    st.subheader("Masukkan Nomor Telepon")
    search_num = st.text_input("Contoh: 08123456789").strip()
    
    if st.button("Periksa Nomor"):
        if not search_num:
            st.warning("Silakan masukkan nomor HP terlebih dahulu!")
        else:
            search_num_clean = re.sub(r'\D', '', search_num)
            if search_num_clean.startswith("62"):
                search_num_clean = "0" + search_num_clean[2:]
                
            if search_num_clean in st.session_state['database_tag']:
                tags = st.session_state['database_tag'][search_num_clean]
                st.success(f"Ditemukan {len(tags)} tag")
                for tag in tags:
                    st.markdown(f'<div class="tag-container"><b>👤 {tag}</b></div>', unsafe_allow_html=True)
            else:
                st.info("Nomor tidak ditemukan di database kami.")

with tab2:
    st.markdown("""
    <div class="info-box">
        <b>💡 Fitur Auto-Parser Aktif:</b> Sekarang kamu bisa langsung mengunggah file <b>.txt</b> hasil edit manual atau file <b>.vcf</b> asli hasil ekspor dari kontak HP kamu tanpa perlu diubah lagi!
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Pilih file kontak (.txt atau .vcf)", type=["txt", "vcf"])
    
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")
        count = 0
        
        # JALUR 1: JIKA USER UPLOAD FILE .VCF ASLI HP
        if uploaded_file.name.endswith('.vcf'):
            # Mencari blok nama (FN:) dan nomor telepon (TEL:) secara berpasangan
            cards = file_contents.split("BEGIN:VCARD")
            for card in cards:
                fn_match = re.search(r"FN:(.*)", card)
                tel_match = re.search(r"TEL;.*:(.*)", card)
                if not tel_match:
                    tel_match = re.search(r"TEL:(.*)", card) # Fallback format vcard lama
                
                if fn_match and tel_match:
                    nama = fn_match.group(1).strip()
                    nomor = re.sub(r'\D', '', tel_match.group(1)) # Ambil angka saja
                    
                    if nomor.startswith("62"):
                        nomor = "0" + nomor[2:]
                    
                    if nomor and nama:
                        if nomor in st.session_state['database_tag']:
                            if nama not in st.session_state['database_tag'][nomor]:
                                st.session_state['database_tag'][nomor].append(nama)
                        else:
                            st.session_state['database_tag'][nomor] = [nama]
                        count += 1
            st.success(f"🔥 Hebat! Berhasil mengekstrak {count} kontak langsung dari file .vcf HP kamu!")
            
        # JALUR 2: JIKA USER UPLOAD FILE .TXT BIASA (Format: nomor,nama)
        elif uploaded_file.name.endswith('.txt'):
            stringio = io.StringIO(file_contents)
            for line in stringio.readlines():
                if "," in line:
                    parts = line.strip().split(",", 1)
                    nomor = re.sub(r'\D', '', parts[0])
                    if nomor.startswith("62"):
                        nomor = "0" + nomor[2:]
                    nama = parts[1].strip()
                    
                    if nomor and nama:
                        if nomor in st.session_state['database_tag']:
                            if nama not in st.session_state['database_tag'][nomor]:
                                st.session_state['database_tag'][nomor].append(nama)
                        else:
                            st.session_state['database_tag'][nomor] = [nama]
                        count += 1
            st.success(f"Berhasil mengimpor {count} kontak dari file .txt!")

st.markdown("---")
st.caption("FitooTag Engine Pro v1.5 | Platform © 2026")
