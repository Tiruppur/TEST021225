import streamlit as st
import pandas as pd

st.set_page_config(page_title="Search App", layout="wide")

# =========================
# CSS (Orange Theme)
# =========================
st.markdown("""
<style>
h2, h3, label, p, span, div {
    color: orange !important;
    font-weight: bold !important;
}

/* Hide DataFrame Download Button */
.stDataFrame div[data-testid="stElementToolbar"] {
    display: none !important;
}

/* Light color placeholder for first option in dropdown */
option:first-child {
    color: #b3b3b3 !important;
}
</style>
""", unsafe_allow_html=True)

# ====================================
# LOAD PARQUET
# ====================================
@st.cache_data
def load_data():
    return pd.read_parquet("data/output.parquet")

df = load_data()

st.title("Search Voter Data")

# ===========================
# RESET BUTTON (WORKS NOW)
# ===========================
if st.button("Reset Search"):
    st.experimental_set_query_params()   # Clears URL params
    st.session_state.clear()             # Clears widgets
    st.rerun()

# ===========================
# AC DROPDOWN WITH PLACEHOLDER
# ===========================
ac_list = sorted(df["AC"].dropna().unique().tolist())

ac_choice = st.selectbox(
    "Select AC",
    ["-- Select AC --"] + ac_list,
    index=0
)

# ===========================
# Search Input
# ===========================
search_value = st.text_input("Enter Voter Number or Name")

# ===========================
# SEARCH BUTTON
# ===========================
if st.button("Search"):
    if ac_choice == "-- Select AC --":
        st.warning("Please select an AC first.")
    else:
        # Apply AC filter
        result = df[df["AC"] == ac_choice]

        # Apply search
        if search_value.strip() != "":
            result = result[
                result.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)
            ]

        # Show results as table
        if len(result) > 0:
            st.dataframe(result, use_container_width=True)
        else:
            st.error("No matching records found.")

