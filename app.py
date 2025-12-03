import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
#     CUSTOM CSS THEME
# ============================
st.markdown("""
<style>

    /* === MAIN BACKGROUND === */
    .stApp {
        background-color: #001f3f !important;   /* Navy Blue */
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background-color: #001a35 !important;
    }

    /* === Global Text Color === */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: white !important;
    }

    /* ============================================
       SELECTBOX (Dropdown) – ORANGE THEME 
       Bigger Font + Bold + Hover Color
       ============================================ */

    /* Selectbox main box */
    .stSelectbox > div > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        color: orange !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }

    /* Dropdown popup list */
    .css-26l3qy-menu, .css-1n7v3ny-option {
        background-color: #00264d !important;
        color: orange !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* Hover effect */
    .css-1n7v3ny-option:hover {
        background-color: #ff8800 !important;  /* Orange highlight */
        color: black !important;
    }

    /* Selected item */
    .css-1n7v3ny-option.is-selected {
        background-color: orange !important;
        color: black !important;
        font-weight: 900 !important;
    }

    /* Text Input Boxes */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: white !important;
        border: 2px solid orange !important;
        border-radius: 6px;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #ff6600 !important;
        color: white !important;
        border-radius: 6px;
        padding: 8px 20px;
        border: 1px solid white;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    .stButton>button:hover {
        background-color: #ff8800 !important;
        border: 1px solid white;
    }

    /* DataFrame background */
    .stDataFrame {
        background-color: white !important;
        border-radius: 8px;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================
#        MAIN APPLICATION LOGIC
# ============================================

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
