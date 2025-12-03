import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# -----------------------
# NAVY BLUE THEME
# -----------------------
st.markdown("""
<style>

    /* === Main App Background === */
    .stApp {
        background-color: #001f3f !important;
    }

    /* === Sidebar Background === */
    section[data-testid="stSidebar"] {
        background-color: #001a35 !important;
    }

    /* === Text Color === */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: white !important;
    }

    /* === Text Input Style === */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: white !important;
        border: 1px solid #0059b3 !important;
        border-radius: 6px;
    }

    /* === Selectbox (Dropdown) - change font color === */
    .stSelectbox>div>div {
        background-color: #00264d !important; /* box background */
        color: white !important;              /* dropdown selected text color */
        border: 1px solid #0059b3 !important;
        border-radius: 6px;
    }

    /* Dropdown list items font color */
    div[data-baseweb="select"] * {
        color: white !important;              /* dropdown menu text */
        background-color: #003366 !important; /* dropdown menu background */
    }

    /* === Buttons === */
    .stButton>button {
        background-color: #004080 !important;
        color: white !important;
        border-radius: 6px;
        padding: 8px 20px;
        border: 1px solid white;
    }

    .stButton>button:hover {
        background-color: #0059b3 !important;
        color: white !important;
    }

    /* === Dataframe Background === */
    .stDataFrame {
        background-color: white !important;
        border-radius: 8px;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------
# App Logic
# -----------------------

def find_col(df, name):
    name = name.lower()
    for col in df.columns:
        if col.lower() == name:
            return col
    for col in df.columns:
        if name in col.lower():
            return col
    return None

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

df = None
csv_path = os.path.join("data", f"{ac_map[selected_ac]}.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error("CSV கிடைக்கவில்லை!")

if df is not None:

    fm = st.text_input("FM_NAME_V2")
    rln = st.text_input("RLN_FM_NAME_V2")

    if st.button("Search"):

        result = df.copy()

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NAME_V2")

        if fm and fm_col:
            result = result[result[fm_col].astype(str).str.contains(fm, case=False, na=False)]

        if rln and rln_col:
            result = result[result[rln_col].astype(str).str.contains(rln, case=False, na=False)]

        st.dataframe(result, use_container_width=True)

    if st.button("Reset"):
        st.rerun()
