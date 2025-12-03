import streamlit as st
import pandas as pd
import os

# ============================
# PAGE CONFIG + BLINK TITLE
# ============================
st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# Blinking Title CSS (2 sec)
st.markdown("""
<style>
#blink-title {
    animation: blink 2s infinite;
}
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0.2;}
    100% {opacity: 1;}
}
</style>

<h1 id="blink-title">திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</h1>
""", unsafe_allow_html=True)



# ============================
# PHONETIC TYPING SCRIPT
# ============================
st.markdown("""
<script src="https://www.google.com/jsapi" type="text/javascript"></script>
<script type="text/javascript">
google.load("elements", "1", {packages: "transliteration"});

function onLoad() {
    var options = {
        sourceLanguage: google.elements.transliteration.LanguageCode.ENGLISH,
        destinationLanguage: ["ta"],    
        transliterationEnabled: true
    };

    var control = new google.elements.transliteration.TransliterationControl(options);

    // APPLY TAMIL PHONETIC FOR THESE INPUT FIELDS
    control.makeTransliteratable(['fm_input', 'rln_input']);
}

google.setOnLoadCallback(onLoad);
</script>
""", unsafe_allow_html=True)



# ============================
# CUSTOM NAVY + ORANGE THEME
# ============================
st.markdown("""
<style>

    .stApp {
        background-color: #001f3f !important;
    }

    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: white !important;
        font-weight: bold;
    }

    /* DROPDOWN BOX */
    div[data-baseweb="select"] > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
    }

    /* Dropdown Text */
    div[data-baseweb="select"] span {
        color: orange !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* Dropdown Menu */
    ul {
        background-color: #001f3f !important;
        border: 1px solid orange !important;
    }

    li {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    li:hover {
        background-color: orange !important;
        color: black !important;
        font-weight: bold !important;
    }

    /* TEXT INPUT BOX STYLE */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* BUTTONS */
    .stButton>button {
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 6px !important;
        border: 2px solid white !important;
        font-weight: bold !important;
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


# ============================
# AC DROPDOWN
# ============================
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
# SEARCH INPUTS
# ============================
if df is not None:

    fm = st.text_input("FM_NAME_V2 (EXACT MATCH)", key="fm_input")
    rln = st.text_input("RLN_FM_NM_V2 (EXACT MATCH)", key="rln_input")

    if st.button("Search"):

        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df.copy()

        # EXACT MATCH — THREE CONDITIONS
        if fm and rln:
            result = result[
                (result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()) &
                (result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower())
            ]

        elif fm:
            result = result[
                result[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()
            ]

        elif rln:
            result = result[
                result[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower()
            ]

        st.dataframe(result, use_container_width=True)


    if st.button("Reset"):
        st.rerun()
