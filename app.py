import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
#  CUSTOM CSS (Navy + Orange + Blink)
# ============================
st.markdown("""
<style>

    .stApp { background-color: #001f3f !important; }

    .blink-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: orange;
        animation: blinker 2s linear infinite;
    }

    @keyframes blinker { 50% { opacity: 0; } }

    h2, h3, label, p, span, div {
        color: white !important;
        font-weight: bold !important;
    }

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

    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    div.stButton > button {
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
    }

    div.stButton > button:hover {
        background-color: #ffa733 !important;
        border: 2px solid yellow !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================
# BLINK TITLE
# ============================
st.markdown("<h1 class='blink-title'>திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</h1>", unsafe_allow_html=True)

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
# AC MAP
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
# LOAD CSV
# ============================
df = None
csv_path = os.path.join("data", f"{ac_map[selected_ac]}.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error("CSV கிடைக்கவில்லை!")

# ============================
# SEARCH SECTION
# ============================
if df is not None:

    fm = st.text_input("FM_NAME_V2 (EXACT MATCH)")
    rln = st.text_input("RLN_FM_NM_V2 (EXACT MATCH)")

    col1, col2, col3 = st.columns([3,2,3])
    with col2:
        colA, colB = st.columns(2)
        with colA:
            search = st.button("Search", use_container_width=True)
        with colB:
            reset = st.button("Reset", use_container_width=True)

    if search:

        # NO EMPTY SEARCH
        if not fm and not rln:
            st.error("FM_NAME_V2 அல்லது RLN_FM_NM_V2 ஆகிய இரண்டில் ஒன்று கட்டாயம் உள்ளிட வேண்டும்!")
            st.stop()

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df.copy()

        # CASE 1: BOTH EXACT MATCH
        if fm and rln:
            result = result[
                (result[fm_col].astype(str).str.lower().str.strip() == fm.lower().strip()) &
                (result[rln_col].astype(str).str.lower().str.strip() == rln.lower().strip())
            ]

        # CASE 2: FM ONLY
        elif fm:
            result = result[
                result[fm_col].astype(str).str.lower().str.strip() == fm.lower().strip()
            ]

        # CASE 3: RLN ONLY
        elif rln:
            result = result[
                result[rln_col].astype(str).str.lower().str.strip() == rln.lower().strip()
            ]

        st.dataframe(result, use_container_width=True)

    if reset:
        st.rerun()

# ===========================================
# ⭐ EXTRA FEATURE → ENGLISH → TAMIL BOX
# ===========================================
st.subheader("English → Tamil Auto Convert")

tamil_box = st.text_area("Type here in English (after SPACE it converts):", key="tam_box")

# JavaScript – Auto Convert English → Tamil
st.markdown("""
<script src="https://www.google.com/jsapi"></script>
<script>
google.load("elements", "1", { packages: "transliteration" });

function onLoad() {
    var options = {
        sourceLanguage: 'en',
        destinationLanguage: ['ta'],
        transliterationEnabled: true
    };

    var control = new google.elements.transliteration.TransliterationControl(options);
    control.makeTransliteratable(['tam_box']);
}

google.setOnLoadCallback(onLoad);
</script>
""", unsafe_allow_html=True)
