import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
#  CUSTOM CSS (Navy + Orange + Blink)
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

    /* LABELS / TEXT WHITE */
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

    /* Selected text inside dropdown */
    div[data-baseweb="select"] span {
        color: orange !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Dropdown menu background */
    ul {
        background-color: #001f3f !important;
        border: 1px solid orange !important;
    }

    /* Dropdown items */
    li {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Hover item */
    li:hover {
        background-color: orange !important;
        color: black !important;
        font-weight: bold !important;
    }

    /* TEXT INPUT BOXES */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* BUTTONS BIG + CENTER */
    .big-btn button {
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 15px 40px !important;
    }

    .big-btn button:hover {
        background-color: #ffa733 !important;
        border: 2px solid yellow !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================
# CENTER BLINK TITLE
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

    fm = st.text_input("FM_NAME_V2 (EXACT MATCH)")
    rln = st.text_input("RLN_FM_NM_V2 (EXACT MATCH)")

    # BUTTONS SIDE BY SIDE & CENTER
    col1, col2, col3 = st.columns([3, 2, 3])

    with col1:
        st.write("")

    with col2:
        search_clicked = st.container()
        reset_clicked = st.container()

        with st.container():
            colA, colB = st.columns(2)

            with colA:
                search = st.button("Search", key="search_btn", use_container_width=True)
            with colB:
                reset = st.button("Reset", key="reset_btn", use_container_width=True)

        # Apply big button CSS
        st.markdown("""
            <style>
                div.stButton > button {
                    background-color: #ff8c00 !important;
                    color: black !important;
                    border-radius: 8px !important;
                    border: 2px solid white !important;
                    font-size: 22px !important;
                    font-weight: bold !important;
                    padding: 12px 40px !important;
                }
            </style>
        """, unsafe_allow_html=True)

    with col3:
        st.write("")

    # ============================
    # SEARCH RESULT
    # ============================
    if search:

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df.copy()

        # BOTH EXACT MATCH
        if fm and rln:
            result = result[
                (result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()) &
                (result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower())
            ]

        # FM ONLY
        elif fm:
            result = result[
                result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()
            ]

        # RLN ONLY
        elif rln:
            result = result[
                result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower()
            ]

        st.dataframe(result, use_container_width=True)

    if reset:
        st.rerun()
