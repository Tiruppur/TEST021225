import streamlit as st
import pandas as pd
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002",
    layout="wide"
)

# -------------------------------
# Custom CSS for ECI Theme
# -------------------------------
st.markdown("""
<style>

body {
    background-color: #F5F5F5;
}

/* Main Title */
.main-title {
    color: #0D47A1;
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 25px;
}

/* Dropdown & Textbox */
.stSelectbox, .stTextInput > label {
    color: #0D47A1 !important;
    font-weight: 600;
}

.stSelectbox div[data-baseweb="select"] {
    border: 2px solid #0D47A1 !important;
    border-radius: 8px;
}

/* Search Inputs */
.stTextInput input {
    border: 2px solid #0D47A1 !important;
    border-radius: 8px;
}

/* Blue Button */
.stButton > button {
    background-color: #0D47A1;
    color: white;
    font-weight: 600;
    padding: 8px 20px;
    border-radius: 8px;
}

/* Page Border Container */
.big-box {
    border: 3px solid #0D47A1;
    border-radius: 12px;
    padding: 25px;
    background-color: white;
    box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown('<div class="main-title">திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</div>', unsafe_allow_html=True)

# -------------------------------
# Start Big Border Box
# -------------------------------
st.markdown('<div class="big-box">', unsafe_allow_html=True)

# -------------------------------
# AC List with Full Names (unchanged)
# -------------------------------
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

ac_list = list(ac_map.keys())

selected_ac = st.selectbox(
    "சட்டமன்ற தொகுதியை தேர்ந்தெடுக்கவும்",
    ac_list,
    index=None,
    placeholder="தேர்ந்தெடுக்கவும்"
)

# -------------------------------
# Helper: find best matching column name
# Searches exact match first, then substring match (case-insensitive)
# -------------------------------
def find_col(df, target_name):
    if df is None:
        return None
    target = target_name.lower()
    # Exact match (case-insensitive)
    for col in df.columns:
        if col.lower() == target:
            return col
    # Substring match (col contains target)
    for col in df.columns:
        if target in col.lower():
            return col
    # Try remove underscores/dashes and compare
    simplified_target = target.replace("_", "").replace("-", "").replace(" ", "")
    for col in df.columns:
        c = col.lower().replace("_", "").replace("-", "").replace(" ", "")
        if c == simplified_target:
            return col
    return None

# -------------------------------
# Load CSV after selecting AC
# -------------------------------
df = None
file_exists = False
if selected_ac:
    ac_number = ac_map[selected_ac]         # Extract “102” from “102-AVN”
    file_path = f"data/{ac_number}.csv"     # Load data/102.csv

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            file_exists = True
        except Exception as e:
            st.error(f"CSV படிக்கும் போது பிழை: {e}")
    else:
        st.error("CSV கோப்பு கிடைக்கவில்லை!")

# -------------------------------
# If data loaded, show search UI
# -------------------------------
if file_exists and df is not None:
   

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        fm_name = st.text_input("FM_NAME_V2 மூலம் தேடல்")
    with col2:
        rln_fm_name = st.text_input("RLN_FM_NAME_V2 மூலம் தேடல்")

    # Buttons: Search | Reset
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        search_clicked = st.button("Search")
    with btn_col2:
        reset_clicked = st.button("Reset")

    if reset_clicked:
        # Simple reset: rerun clears inputs
        st.experimental_rerun()

    results_shown = False
    if search_clicked:
        # require at least one input to search
        if not fm_name and not rln_fm_name:
            st.warning("தேட Search செய்ய ஏ Minimum ஒரு வை என்னும் உள்ளீட்டை இடவும்.")
        else:
            result = df.copy()

            # FM_NAME_V2 detection & filter
            if fm_name:
                fm_col = find_col(df, "FM_NAME_V2")
                if fm_col:
                    result = result[result[fm_col].astype(str).str.contains(fm_name, case=False, na=False)]
                else:
                    st.warning("⚠ FM_NAME_V2 போன்ற ஒரு column இந்த CSV-ல் காணப்படவில்லை.")
                    st.info("இந்த CSV-வில் உள்ள columns:", icon="ℹ️")
                    st.write(list(df.columns))

            # RLN_FM_NAME_V2 detection & filter
            if rln_fm_name:
                rln_col = find_col(df, "RLN_FM_NAME_V2")
                if rln_col:
                    result = result[result[rln_col].astype(str).str.contains(rln_fm_name, case=False, na=False)]
                else:
                    st.warning("⚠ RLN_FM_NAME_V2 போன்ற ஒரு column இந்த CSV-ல் காணப்படவில்லை.")
                    st.info("இந்த CSV-வில் உள்ள columns:", icon="ℹ️")
                    st.write(list(df.columns))

            # Show results
            st.write("### தேடல் முடிவு")
            st.write(f"மொத்தம் முடிவுகள்: *{len(result)}*")
            st.dataframe(result, use_container_width=True)

            # Download as CSV
            if len(result) > 0:
                csv_bytes = result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download filtered results as CSV",
                    data=csv_bytes,
                    file_name=f"results_{ac_number}.csv",
                    mime="text/csv"
                )

            results_shown = True

    # if no search yet, show hint
    if not results_shown:
        st.info("Search பொத்தானை அழுத்தி தேடுங்கள் — அல்லது Reset பொத்தானை அழுத்தி மீண்டும் தொடங்குங்கள்.")

# -------------------------------
# End Box
# -------------------------------
st.markdown('</div>', unsafe_allow_html=True)

