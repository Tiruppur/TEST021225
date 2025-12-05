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
        color: orange !important;
        font-weight: bold !important;
        }

      h2, h3,  p, span, div {
        color: white !important;
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
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 8px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
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

selected_ac = st.selectbox("சட்டமன்றத் தொகுதியை தேர்வு செய்யவும்", list(ac_map.keys()), index=0)

# ==================================
# LOAD PARQUET (FAST + SMALL)
# ==================================
df = None
parquet_path = os.path.join("data", f"{ac_map[selected_ac]}.parquet")

if os.path.exists(parquet_path):
    df = pd.read_parquet(parquet_path)
else:
    st.error("Parquet file கிடைக்கவில்லை!")
    st.stop()

# ==================================
# SEARCH INPUT
# ==================================
fm = st.text_input("வாக்காளரின் பெயர் (EXACT MATCH - 2002 பட்டியல்படி)")
rln = st.text_input("உறவினர் பெயர் (EXACT MATCH - 2002 பட்டியல்படி)")

col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    colA, colB = st.columns(2)
    with colA: search = st.button("Search", use_container_width=True)
    with colB: reset = st.button("Reset", use_container_width=True)

# ==================================
# EXECUTE SEARCH
# ==================================
if search:

    if not fm and not rln:
        st.error("பெயர் அல்லது உறவினர் பெயரில் ஒன்றையாவது உள்ளிடவும்!")
        st.stop()

    fm_col = find_col(df, "FM_NAME_V2")
    rln_col = find_col(df, "RLN_FM_NM_V2")

    if not fm_col or not rln_col:
        st.error("CSV/Parquet Column names பொருந்தவில்லை! Column headers-ஐ சரிபார்க்கவும்.")
        st.stop()

    fm_clean = clean_text(fm)
    rln_clean = clean_text(rln)

    temp = df.copy()
    temp["_fm"] = temp[fm_col].apply(clean_text)
    temp["_rln"] = temp[rln_col].apply(clean_text)

    if fm and rln:
        result = temp[(temp["_fm"] == fm_clean) & (temp["_rln"] == rln_clean)]
    elif fm:
        result = temp[temp["_fm"] == fm_clean]
    else:
        result = temp[temp["_rln"] == rln_clean]

    if result.empty:
        st.warning("தகவல் எதுவும் கிடைக்கவில்லை. 2002 spelling-ஐ சரிபார்க்கவும்.")
    else:
        st.dataframe(result.drop(columns=["_fm", "_rln"]), use_container_width=True)

if reset:
    st.rerun()


