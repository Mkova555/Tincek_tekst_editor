import streamlit as st
from streamlit_jodit import st_jodit
import PyPDF2
import base64
import re
from io import BytesIO
from xhtml2pdf import pisa

st.set_page_config(page_title="Tinček Editor PRO", page_icon="ikona.ico", layout="centered")

# Funkcija za pretvaranje teksta u PDF
def stvori_pdf(html_sadrzaj):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 2cm; }}
            body {{ font-family: Helvetica, sans-serif; font-size: 14pt; }}
        </style>
    </head>
    <body>
        {html_sadrzaj}
    </body>
    </html>
    """
    rezultat = BytesIO()
    pisa.CreatePDF(BytesIO(html_template.encode('utf-8')), dest=rezultat, encoding='utf-8')
    return rezultat.getvalue()

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0f !important;
        color: #ffffff !important;
    }
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

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
        box-shadow: 0 6px 8px rgba(147, 51, 234, 0.2) !important;
    }
    
    [data-testid="stFileUploader"] { background-color: transparent !important; }
    [data-testid="stFileUploadDropzone"] {
        background-color: #1a0b2e !important;
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        background-color: #2d134d !important;
        border: 1px solid #9333ea !important;
    }
    [data-testid="stFileUploadDropzone"] div, [data-testid="stFileUploadDropzone"] span, [data-testid="stFileUploadDropzone"] small { color: #d1b3ff !important; }
    [data-testid="stFileUploadDropzone"] svg { fill: #d1b3ff !important; }
    [data-testid="stFileUploadDropzone"] button {
        background-color: #3b176b !important;
        color: #ffffff !important;
        border: 1px solid #a855f7 !important;
        border-radius: 6px !important;
        padding: 4px 12px !important;
    }
    
    [data-testid="stFileUploaderFile"] {
        background-color: #2d134d !important;
        border: 1px solid #9333ea !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderFileName"] { color: white !important; }

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
    
    /* ZAVRŠNI POPRAVAK OKVIRA EDITORA DA BUDE KAO GORNJI OKVIRI */
    iframe {
        border: 1px solid #6b21a8 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        background-color: #1a0b2e !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Tinček Editor PRO")

if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

tab1, tab2 = st.tabs(["📄 Dokumenti", "🖼️ Slike"])

with tab1:
    uploaded_doc = st.file_uploader("Odaberi dokument (PDF ili TXT)", type=["pdf", "txt"])
    if uploaded_doc is not None:
        if uploaded_doc.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_doc)
            izvuceni_tekst = ""
            for stranica in pdf_reader.pages:
                tekst = stranica.extract_text()
                if tekst: izvuceni_tekst += tekst + "<br>"
            if st.button("📑 Učitaj PDF u editor"):
                st.session_state.moj_tekst += izvuceni_tekst
                st.rerun()

        elif uploaded_doc.name.endswith('.txt'):
            tekst_iz_fajla = uploaded_doc.getvalue().decode("utf-8")
            if st.button("📝 Učitaj TXT u editor"):
                st.session_state.moj_tekst += tekst_iz_fajla.replace('\n', '<br>')
                st.rerun()

with tab2:
    uploaded_img = st.file_uploader("Odaberi sliku iz galerije", type=["png", "jpg", "jpeg"])
    if uploaded_img is not None:
        if st.button("✨ Umetni sliku u tekst"):
            base64_slika = base64.b64encode(uploaded_img.getvalue()).decode("utf-8")
            format_slike = uploaded_img.name.split('.')[-1]
            img_tag = f'<br><img src="data:image/{format_slike};base64,{base64_slika}" style="max-width: 100%; border-radius: 8px; border: 1px solid #9333ea;"><br>'
            st.session_state.moj_tekst += img_tag
            st.rerun()

st.divider()

# Forsiramo prave tamne boje i bijele tipke unutar samog editora
postavke = {
    'minHeight': 500,
    'theme': 'dark',
    'style': {
        'background': '#1a0b2e', # Ista tamno ljubičasta kao okviri
        'color': '#ffffff'
    }
}

tekst = st_jodit(value=st.session_state.moj_tekst, config=postavke)

if tekst:
    st.session_state.moj_tekst = tekst

st.divider()

st.markdown("### 💾 Spremi dokument")
st.caption("Odaberi u kojem formatu želiš preuzeti svoj tekst:")

# Više opcija preuzimanja podijeljenih u stupce
col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(label="🌐 Izvorni (HTML)", data=tekst, file_name="dokument.html", mime="text/html")

with col2:
    # Čišćenje HTML tagova za čisti tekst
    cisti_tekst = re.sub(r'<[^>]+>', '\n', tekst).replace('&nbsp;', ' ')
    st.download_button(label="📄 Čisti tekst", data=cisti_tekst, file_name="dokument.txt", mime="text/plain")

with col3:
    try:
        pdf_bajtovi = stvori_pdf(tekst)
        st.download_button(label="📑 PDF", data=pdf_bajtovi, file_name="dokument.pdf", mime="application/pdf")
    except Exception as e:
        # Ako je neka ogromna slika ubačena i PDF pukne, javljamo grešku
        st.download_button(label="📑 PDF", data=b'', file_name="prazno.pdf", disabled=True, help="Ukloni složene slike za PDF")

st.divider()

if st.button("🗑️ Obriši sav tekst iz editora"):
    st.session_state.moj_tekst = ""
    st.rerun()