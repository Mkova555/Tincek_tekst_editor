import streamlit as st

st.set_page_config(page_title="Tinček Editor", layout="centered")

# ISPRAVLJENO: Ovdje je bila greška, sada piše unsafe_allow_html=True
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Tinček Editor")

# Pamćenje teksta
if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

# Standardni, neuništivi prostor za unos teksta
tekst = st.text_area(
    "Počni pisati ispod:", 
    value=st.session_state.moj_tekst, 
    height=400,
    placeholder="Tvoj tekst ide ovdje..."
)

# Spremanje
if tekst:
    st.session_state.moj_tekst = tekst

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="📥 Preuzmi tekst",
        data=tekst,
        file_name="moj_dokument.txt",
        mime="text/plain",
    )

with col2:
    if st.button("🗑️ Obriši sve"):
        st.session_state.moj_tekst = ""
        st.rerun()