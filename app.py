import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
#  CUSTOM CSS
# ============================
st.markdown("""
<style>

    /* PAGE BACKGROUND */
    .stApp {
        background-color: #001f3f !important;
    }

    /* CENTER + BLINK TITLE */
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

    /* TEXT COLOR WHITE */
    h2, h3, label, p, span, div {
        color: white !important;
        font-weight: bold !important;
    }

    /* DROPDOWN BOX */
    div[data-baseweb="select"] > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="select"] span {
        color: orange !important;
        font-size: 18px !important;
    }

    /* BUTTON STYLE */
    .big-center-btn button {
        width: 220px !important;
        height: 60px !important;
        font-size: 22px !important;
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 10px !important;
        border: 3px solid white !important;
        font-weight: bold !important;
    }

    .big-center-btn button:hover {
        background-color: #ffa733 !important;
        border: 3px solid yellow !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================
# CENTER BLINK TITLE
# ============================
st.markdown("<h1 class='blink-title'>திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</h1>", unsafe_allow_html=True)

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

# ============================
# Load CSV
# ============================
df = None
csv_path = os.path.join("data", f"{ac_map[selected_ac]}.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error("CSV கிடைக்கவில்லை!")

# ============================
# SEARCH LOGIC
# ============================
if df is not None:

    fm = st.text_input("FM_NAME_V2 (EXACT MATCH) — கட்டாயம் உள்ளிடவும்")
    rln = st.text_input("RLN_FM_NM_V2 (EXACT MATCH — OPTIONAL)")

    # ========== BUTTONS CENTER ==========
    colA, colB, colC = st.columns([1,1,1])

    with colB:
        s
