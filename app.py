import streamlit as st
from streamlit_jodit import st_jodit
import PyPDF2
import base64

# Postavke stranice
st.set_page_config(page_title="Tinček Editor PRO", layout="centered")

# BRUTALNI CSS Koji gazi sve Streamlitove defaultne stilove i zaključava tvoj dizajn!
st.markdown("""
    <style>
    /* Pozadina i tekst cijele aplikacije */
    .stApp {
        background-color: #0b0b0f !important;
        color: #ffffff !important;
    }
    
    /* Skrivanje nepotrebnih menija */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    /* SVI gumbi (i obični i onaj za download) moraju biti ljubičasti */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #1a0b2e !important;
        color: #d1b3ff !important;
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #2d134d !important;
        border: 1px solid #9333ea !important;
        color: white !important;
    }
    
    /* Popravak onog ružnog okvira kod učitavanja fajlova */
    [data-testid="stFileUploadDropzone"] {
        background-color: #11081f !important;
        border: 1px dashed #6b21a8 !important;
        color: #d1b3ff !important;
    }
    [data-testid="stFileUploadDropzone"] * {
        color: #d1b3ff !important;
    }

    /* Tabovi (kartice za Dokumente i Slike) */
    [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #a3a3a3 !important;
    }
    [aria-selected="true"] {
        border-bottom-color: #9333ea !important;
        color: #d1b3ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Tinček Editor PRO")

if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

# ZONA ZA UČITAVANJE
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
            base64_slika = base64.b64encode(uploaded_img.getvalue()).decode("utf-8")
            format_slike = uploaded_img.name.split('.')[-1]
            img_tag = f'<br><img src="data:image/{format_slike};base64,{base64_slika}" style="max-width: 100%; border-radius: 8px;"><br>'
            st.session_state.moj_tekst += img_tag
            st.rerun()

st.divider()

# Prisiljavamo Word editor da bude zaista crn, a ne onako sivi
postavke = {
    'minHeight': 500,
    'theme': 'dark',
    'style': {
        'background': '#0b0b0f', 
        'color': '#ffffff'
    }
}

tekst = st_jodit(value=st.session_state.moj_tekst, config=postavke)

if tekst:
    st.session_state.moj_tekst = tekst

st.divider()

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