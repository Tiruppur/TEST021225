import streamlit as st
import pandas as pd
import os
import unicodedata

st.set_page_config(page_title="திருப்பூர் மாவட்டம்  வாக்காளர் விபரம் 2002", layout="wide")

# ==================================
# CUSTOM DARK THEME + ORANGE
# ==================================
st.markdown("""
<style>

    .stApp {
        background-color: #001f3f !important;
    }

    .blink-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: orange;
        animation: blinker 2s linear infinite;
    }

    @keyframes blinker {
        50% { opacity: 0; }
    }

    label div {
        color: white !important;
        font-weight: bold !important;
    }

    h2, h3, p, span, div {
        color: orange !important;
        font-weight: bold !important;
    }

    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    div.stButton > button {
        background-color: #FFFFFF !important;
        color: black !important;
        border-radius: 8px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
    }

    /* Hide dataframe download and menu */
    .stDataFrame div[data-testid="stElementToolbar"] {
        display: none !important;
    }

</style>
""", unsafe_allow_html=True)

# ==================================
# TITLE
# ==================================
st.markdown("<h1 class='blink-title'>திருப்பூர் மாவட்டம் --> வாக்காளர் விபரம் 2002</h1>", unsafe_allow_html=True)

# ==================================
# Helper — Clean Tamil Text
# ==================================
def clean_text(val):
    if pd.isna(val):
        return ""
    return unicodedata.normalize("NFC", str(val).strip().lower())

def find_col(df, name):
    name = name.lower()
    for col in df.columns:
        if col.lower() == name:
            return col
    for col in df.columns:
        if name in col.lower():
            return col
    return None

# ==================================
# AC MAP
# ==================================
ac_map = {
    "102-அவினாசி": "102",
    "111-உடுமலைபேட்டை": "111",
    "112-தாராபுரம்": "112",
    "113-வெள்ளகோவில்": "113",
    "114-பொங்கலூர்": "114",
    "115-பல்லடம்": "115",
    "116-திருப்பூர்": "116",
    "117-காங்கேயம்": "117"
}

# ==================================
# AC SELECTBOX (Default = Select AC)
# ==================================
selected_ac = st.selectbox(
    "சட்டமன்றத் தொகுதியை தேர்வு செய்யவும்",
    ["Select AC"] + list(ac_map.keys()),
    index=0
)

if selected_ac == "Select A_
