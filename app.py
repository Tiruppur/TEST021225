import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

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

        st.write("### Column Search Filters")

        # ---- Per Column Search ----
        col_inputs = {}
        col_blocks = st.columns(len(result.columns))

        for i, col in enumerate(result.columns):
            col_inputs[col] = col_blocks[i].text_input(f"{col} தேடு")

        filtered = result.copy()
        for col, val in col_inputs.items():
            if val:
                filtered = filtered[filtered[col].astype(str).str.contains(val, case=False, na=False)]

        # Display filtered result
        st.dataframe(filtered, use_container_width=True)

    if st.button("Reset"):
        st.rerun()
