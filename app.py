import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
# CUSTOM NAVY + ORANGE THEME
# ============================
st.markdown("""
<style>

    /* Main App Background */
    .stApp {
        background-color: #001f3f !important;
    }

    /* Text Colors */
    h1, h2, h3, h4, label, p, span, div {
        color: white !important;
        font-weight: bold;
    }

    /* DROPDOWN BOX STYLE */
    div[data-baseweb="select"] > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
    }

    /* Dropdown Selected Text */
    div[data-baseweb="select"] span {
        color: orange !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Dropdown Menu List Background */
    ul {
        background-color: #001f3f !important;
        border: 1px solid orange !important;
    }

    /* Dropdown Items */
    li {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* DROPDOWN HOVER EFFECT */
    li:hover {
        background-color: orange !important;
        color: black !important;
        font-weight: bold !important;
    }

    /* Text Input Boxes */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        border: 2px solid white !important;
    }

    .stButton>button:hover {
        background-color: #ffa733 !important;
        color: black !important;
        border: 2px solid yellow !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================
# HELPER FUNCTION
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
# AC Mapping
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


st.title("திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002")

selected_ac = st.selectbox("AC தேர்வு", list(ac_map.keys()), index=0)

# ============================
# LOAD CSV
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

    if st.button("Search"):

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df.copy()

        # -----------------------
        # EXACT MATCH LOGIC
        # -----------------------

        # 1️⃣ If BOTH fields entered → Exact match for both
        if fm and rln:
            result = result[
                (result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()) &
                (result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower())
            ]

        # 2️⃣ Only FM entered → Exact match for FM
        elif fm:
            result = result[
                result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()
            ]

        # 3️⃣ Only RLN entered → Exact match for RLN
        elif rln:
            result = result[
                result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower()
            ]

        st.dataframe(result, use_container_width=True)

    if st.button("Reset"):
        st.rerun()
