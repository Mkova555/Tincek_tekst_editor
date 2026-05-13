import streamlit as st
from streamlit_jodit import st_jodit
import PyPDF2
import base64
import re
from io import BytesIO
from xhtml2pdf import pisa

# 1. OSNOVNE POSTAVKE I IKONA
st.set_page_config(
    page_title="Tinček Editor PRO", 
    page_icon="ikona.ico", 
    layout="centered"
)

# 2. FUNKCIJA ZA GENERIRANJE PDF-a
def stvori_pdf(html_sadrzaj):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 2cm; }}
            body {{ font-family: Helvetica, sans-serif; font-size: 12pt; color: black; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        {html_sadrzaj}
    </body>
    </html>
    """
    rezultat = BytesIO()
    pisa_status = pisa.CreatePDF(
        BytesIO(html_template.encode('utf-8')), 
        dest=rezultat, 
        encoding='utf-8'
    )
    return rezultat.getvalue()

# 3. BRUTALNI CSS ZA DIZAJN (Ljubičasto-crna tema)
st.markdown("""
    <style>
    /* Pozadina cijele aplikacije */
    .stApp {
        background-color: #0b0b0f !important;
        color: #ffffff !important;
    }
    
    /* Skrivanje Streamlit suvišnih stvari */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    /* DIZAJN GUMBA (Glavni i Download) */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #1a0b2e !important;
        color: #d1b3ff !important;
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: bold !important;
        padding: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #2d134d !important;
        border: 1px solid #9333ea !important;
        color: white !important;
    }
    
    /* UPLOADER (Okvir za dokumente i slike) */
    [data-testid="stFileUploader"] { background-color: transparent !important; }
    [data-testid="stFileUploadDropzone"] {
        background-color: #1a0b2e !important;
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    [data-testid="stFileUploadDropzone"] div, 
    [data-testid="stFileUploadDropzone"] span, 
    [data-testid="stFileUploadDropzone"] small { color: #d1b3ff !important; }
    [data-testid="stFileUploadDropzone"] svg { fill: #d1b3ff !important; }
    
    /* Gumb 'Browse' unutar uploadera */
    [data-testid="stFileUploadDropzone"] button {
        background-color: #3b176b !important;
        color: #ffffff !important;
        border: 1px solid #a855f7 !important;
    }

    /* TABOVI NA VRHU (Pretvoreni u gumbe) */
    button[data-baseweb="tab"] {
        background-color: #1a0b2e !important;
        color: #d1b3ff !important;
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        margin-right: 10px !important;
        padding: 8px 16px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #3b176b !important;
        border: 2px solid #a855f7 !important;
        color: white !important;
    }
    div[data-baseweb="tab-highlight"] { display: none !important; }
    
    /* OKVIR EDITORA (da bude isti kao gornji okviri) */
    iframe[title="streamlit_jodit.st_jodit"] {
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Tinček Editor PRO")

# 4. LOGIKA ZA PAMĆENJE TEKSTA
if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

# 5. TABOVI ZA UNOS
tab1, tab2 = st.tabs(["📄 Dokumenti", "🖼️ Slike"])

with tab1:
    uploaded_doc = st.file_uploader("Učitaj PDF ili TXT", type=["pdf", "txt"])
    if uploaded_doc:
        if uploaded_doc.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_doc)
            tekst_iz_pdf = ""
            for page in pdf_reader.pages:
                tekst_iz_pdf += page.extract_text() + "<br>"
            if st.button("📑 Ubaci PDF tekst u editor"):
                st.session_state.moj_tekst += tekst_iz_pdf
                st.rerun()
        else:
            txt_sadrzaj = uploaded_doc.getvalue().decode("utf-8")
            if st.button("📝 Ubaci TXT u editor"):
                st.session_state.moj_tekst += txt_sadrzaj.replace('\n', '<br>')
                st.rerun()

with tab2:
    uploaded_img = st.file_uploader("Dodaj sliku", type=["png", "jpg", "jpeg"])
    if uploaded_img:
        if st.button("✨ Umetni sliku u tekst"):
            b64 = base64.b64encode(uploaded_img.getvalue()).decode()
            ext = uploaded_img.name.split('.')[-1]
            img_html = f'<br><img src="data:image/{ext};base64,{b64}" style="max-width:100%; border-radius:8px;"><br>'
            st.session_state.moj_tekst += img_html
            st.rerun()

st.divider()

# 6. POSTAVKE EDITORA (Prisiljavamo bijele tipke i ljubičastu pozadinu)
editor_postavke = {
    "minHeight": 500,
    "theme": "dark", 
    "toolbarAdaptive": False,
    "style": {
        "background": "#1a0b2e",
        "color": "#ffffff",
        "border": "none"
    }
}

tekst_iz_editora = st_jodit(
    value=st.session_state.moj_tekst, 
    config=editor_postavke
)

# Spremanje promjena
if tekst_iz_editora:
    st.session_state.moj_tekst = tekst_iz_editora

st.divider()

# 7. SEKCIJA ZA SPREMANJE (3 Opcije)
st.markdown("### 💾 Spremi dokument")
c1, c2, c3 = st.columns(3)

with c1:
    st.download_button("🌐 HTML", data=tekst_iz_editora, file_name="tekst.html", mime="text/html")

with c2:
    cisti_tekst = re.sub('<[^<]+?>', '', tekst_iz_editora)
    st.download_button("📄 TXT", data=cisti_tekst, file_name="tekst.txt", mime="text/plain")

with c3:
    try:
        pdf_file = stvori_pdf(tekst_iz_editora)
        st.download_button("📑 PDF", data=pdf_file, file_name="dokument.pdf", mime="application/pdf")
    except:
        st.error("Greška kod PDF-a (vjerojatno prevelika slika)")

st.divider()

if st.button("🗑️ Obriši sve"):
    st.session_state.moj_tekst = ""
    st.rerun()