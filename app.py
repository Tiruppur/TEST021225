import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# ============================
# CUSTOM CSS
# ============================
st.markdown("""
<style>

.stApp {
    background-color: #001f3f !important;
}


/* BLINKING TITLE */
.blink-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: orange;
    animation: blinker 2s linear infinite;
}
@keyframes blinker { 50% { opacity: 0; } }


/* Input Box */
.stTextInput>div>div>input {
    background-color: #00264d !important;
    color: orange !important;
    border: 2px solid orange !important;
    border-radius: 6px !important;
    font-size: 18px !important;
    font-weight: bold !important;
}


/* BUTTONS — BIG + CENTER */
.center-buttons {
    display: flex;
    justify-content: center;
    gap: 40px;
}

.big-btn {
    background-color: #ff8c00 !important;
    color: black !important;
    border-radius: 10px !important;
    border: 2px solid white !important;
    padding: 15px 50px !important;
    font-size: 25px !important;
    font-weight: bold !important;
}

.big-btn:hover {
    background-color: #ffa733 !important;
    border: 2px solid yellow !important;
}

</style>
""", unsafe_allow_html=True)

# ============================
# TITLE
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
# Load CSV
# ============================
csv_path = os.path.join("data", f"{ac_map[selected_ac]}.csv")

if not os.path.exists(csv_path):
    st.error("CSV கிடைக்கவில்லை!")
    st.stop()

df = pd.read_csv(csv_path)

# ============================
# SEARCH INPUT
# ============================
fm = st.text_input("FM_NAME_V2 (EXACT MATCH)")
rln = st.text_input("RLN_FM_NM_V2 (EXACT MATCH)")

# ============================
# BUTTONS (CENTER)
# ============================
st.markdown('<div class="center-buttons">', unsafe_allow_html=True)

search = st.button("Search", key="search_btn")
reset = st.button("Reset", key="reset_btn")

st.markdown('</div>', unsafe_allow_html=True)

# Apply button styling
st.markdown("""
<style>
#search_btn button, #reset_btn button {
    background-color: #ff8c00 !important;
    color: black !important;
    border-radius: 10px !important;
    border: 2px solid white !important;
    padding: 15px 50px !important;
    font-size: 25px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ============================
# SEARCH LOGIC (COMPULSORY BOTH FIELDS)
# ============================
if search:

    if not fm.strip() or not rln.strip():
        st.warning("⚠️ தயவு செய்து FM_NAME_V2 மற்றும் RLN_FM_NM_V2 இரண்டையும் உள்ளிடவும்!")
    else:
        fm_col = find_col(df, "FM_NAME_V2")
        rln_col = find_col(df, "RLN_FM_NM_V2")

        result = df[
            (df[fm_col].astype(str).str.strip().str.lower() == fm.strip().lower()) &
            (df[rln_col].astype(str).str.strip().str.lower() == rln.strip().lower())
        ]

        st.dataframe(result, use_container_width=True)

if reset:
    st.rerun()
