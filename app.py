import streamlit as st
from streamlit_jodit import st_jodit
import PyPDF2
import base64

# Postavke stranice
st.set_page_config(page_title="Tinček Editor PRO", layout="centered")

# CSS za mračni dizajn
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0f;
        color: #ffffff;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div.stButton > button {
        background-color: #1a0b2e;
        color: #d1b3ff;
        border: 1px solid #6b21a8;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #2d134d;
        border: 1px solid #9333ea;
        color: white;
    }
    
    .stFileUploader {
        background-color: #11081f;
        border: 1px dashed #6b21a8;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Tinček Editor PRO")

if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

# ZONA ZA UČITAVANJE (podijeljeno u dva taba zbog uštede prostora na mobitelu)
tab1, tab2 = st.tabs(["📄 Dokumenti (PDF/TXT)", "🖼️ Slike"])

with tab1:
    uploaded_doc = st.file_uploader("Odaberi dokument...", type=["pdf", "txt"])
    if uploaded_doc is not None:
        if uploaded_doc.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_doc)
            izvuceni_tekst = ""
            for stranica in pdf_reader.pages:
                tekst = stranica.extract_text()
                if tekst:
                    izvuceni_tekst += tekst + "<br>"
            if st.button("Učitaj PDF u editor"):
                st.session_state.moj_tekst += izvuceni_tekst
                st.rerun()

        elif uploaded_doc.name.endswith('.txt'):
            tekst_iz_fajla = uploaded_doc.getvalue().decode("utf-8")
            if st.button("Učitaj TXT u editor"):
                st.session_state.moj_tekst += tekst_iz_fajla.replace('\n', '<br>')
                st.rerun()

with tab2:
    uploaded_img = st.file_uploader("Odaberi sliku iz galerije...", type=["png", "jpg", "jpeg"])
    if uploaded_img is not None:
        if st.button("Umetni sliku u tekst"):
            # Pretvaranje slike u format koji se može prikazati unutar teksta
            base64_slika = base64.b64encode(uploaded_img.getvalue()).decode("utf-8")
            format_slike = uploaded_img.name.split('.')[-1]
            # HTML tag za sliku koji se prilagođava širini ekrana na mobitelu
            img_tag = f'<br><img src="data:image/{format_slike};base64,{base64_slika}" style="max-width: 100%; border-radius: 8px;"><br>'
            st.session_state.moj_tekst += img_tag
            st.rerun()

st.divider()

# Postavke za Word editor
postavke = {
    'minHeight': 500,
    'theme': 'dark'
}

# Pravi Word editor
tekst = st_jodit(value=st.session_state.moj_tekst, config=postavke)

if tekst:
    st.session_state.moj_tekst = tekst

st.divider()

# Akcije ispod editora
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="📥 Preuzmi dokument",
        data=tekst,
        file_name="moj_dokument.html",
        mime="text/html",
    )

with col2:
    if st.button("🗑️ Obriši sve"):
        st.session_state.moj_tekst = ""
        st.rerun()