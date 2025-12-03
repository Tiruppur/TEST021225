import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
#  TAMIL PHONETIC JS
# ============================
st.markdown("""
<script src="https://www.gstatic.com/inputtools/js/ln/1/en/tamil.js"></script>
<script>
function enableTamilPhonetic() {
    const boxes = document.querySelectorAll("input[type='text']");
    boxes.forEach(box => {
        box.addEventListener("keyup", function(e) {
            if (e.key === " ") {
                this.value = transliterate(this.value);
            }
        });
    });
}

function transliterate(text) {
    try {
        return google.elements.transliteration.Transliterator.transliterate(text);
    } catch(e) {
        return text;
    }
}

setTimeout(enableTamilPhonetic, 1500);
</script>
""", unsafe_allow_html=True)

# ============================
#  CUSTOM CSS
# ============================
st.markdown("""
<style>

    .stApp { background-color:#001f3f !important; }

    .blink-title {
        text-align:center;
        font-size:48px;
        font-weight:bold;
        color:orange;
        animation:blinker 2s linear infinite;
    }
    @keyframes blinker { 50% { opacity:0; } }

    label, p, span, div { color:white !important; font-weight:bold !important; }

    div[data-baseweb="select"] > div {
        background-color:#00264d !important;
        border:2px solid orange !important;
        border-radius:6px;
    }
    div[data-baseweb="select"] span {
        color:orange !important;
        font-size:18px !important;
        font-weight:bold !important;
    }

    .stTextInput>div>div>input {
        background:#00264d !important;
        color:orange !important;
        border:2px solid orange !important;
        font-size:18px !important;
        font-weight:bold !important;
    }

    div.stButton > button {
        background-color:#ff8c00 !important;
        color:black !important;
        border-radius:8px !important;
        border:2px solid white !important;
        font-size:22px !important;
        font-weight:bold !important;
        padding:12px 40px !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================
# BLINK TITLE
# ============================
st.markdown(
    "<h1 class='blink-title'>திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</h1>",
    unsafe_allow_html=True
)

# ============================
# Helper function
# ============================
def find_col(df, name):
    name = name.lower()
    for col in df.columns:
        if col.lower() == name:
            return col
    for col in df.columns:
        if name in col.lower():
            return col
    return None

# ============================
# AC Map
# ============================
ac_map = {
    "102-AVN": "102",
    "111-UDM": "111",
    "112-DPM": "112",
    "113-VEL": "113",
    "114-PON": "114",
    "115-PDM": "115",
    "116-TPR": "116",
    "117-KGM": "117"
}

selected_ac = st.selectbox("AC தேர்வு", list(ac_map.keys()), index=0)

#
