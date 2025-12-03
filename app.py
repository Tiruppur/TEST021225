import streamlit as st
import pandas as pd
import os
from indic_transliteration.sanscript import transliterate, ITAM, TAMIL

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")


# ============================
# CUSTOM ORANGE THEME
# ============================
st.markdown("""
<style>
    .stApp { background-color: #001f3f !important; }
    h1, h2, h3, label, p, span, div { color: white !important; font-weight: bold; }

    /* Dropdown */
    div[data-baseweb="select"] > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] span {
        color: orange !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    ul {
        background-color: #001f3f !important;
        border: 1px solid orange !important;
    }
    li { color: white !important; font-size: 18px !important; font-weight: bold !important; }
    li:hover { background-color: orange !important; color: black !important; font-weight: bold !important; }

    /* Text box style */
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
# Helper
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
csv_path = os.path.join("data", f"{ac_map[selected_ac]}.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error("CSV கிடைக்கவில்லை!")
    df = None



# ============================
# PHONETIC INPUT FUNCTION
# ============================
def phonetic_convert(eng_text):
    if not eng_text:
        return ""
    return transliterate(eng_text, ITAM, TAMIL)



# ============================
# SEARCH LOGIC
# ============================
if df is not None:

    # English → Tamil phonetic typing
    fm_eng = st.text_input("FM_NAME_V2 (Type English → Tamil)")
    rln_eng = st.text_input("RLN_FM_NM_V2 (Type English → Tamil)")

    fm = phonetic_convert(fm_eng)
    rln = phonetic_convert(rln_eng)

    st.write(f"👉 Tamil FM: **{fm}**")
    st.write(f"👉 Tamil RLN: **{rln}**")

    if st.button("Search"):

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df.copy()

        # EXACT MATCH LOGIC
        if fm and rln:
            result = result[
                (result[fm_col].astype(str).str.strip().str.lower() == fm.lower()) &
                (result[rln_col].astype(str).str.strip().str.lower() == rln.lower())
            ]

        elif fm:
            result = result[result[fm_col].astype(str).str.strip().str.lower() == fm.lower()]

        elif rln:
            result = result[result[rln_col].astype(str).str.strip().str.lower() == rln.lower()]

        st.dataframe(result, use_container_width=True)


    if st.button("Reset"):
        st.rerun()
