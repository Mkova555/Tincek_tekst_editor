import streamlit as st
from streamlit_jodit import st_jodit

# Postavke stranice
st.set_page_config(page_title="Tinček Editor", layout="centered")

# Skrivamo suvišne menije da izgleda kao prava aplikacija na mobitelu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("📝 Tinček Editor")

# Pamćenje teksta da se ne obriše prilikom rotacije ekrana
if "moj_tekst" not in st.session_state:
    st.session_state.moj_tekst = ""

# Postavke za Word editor (npr. početna visina)
postavke = {
    'minHeight': 450,
}

# Pravi Word editor s gumbima
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