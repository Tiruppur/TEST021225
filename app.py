# app.py
import streamlit as st
import pandas as pd
import os
import json
from streamlit.components.v1 import html as components_html

st.set_page_config(page_title="திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002", layout="wide")

# -------------------------
# CSS Theme (Navy + Orange)
# -------------------------
st.markdown("""
<style>
    /* PAGE BG */
    .stApp { background-color: #001f3f !important; }

    /* CENTER + BLINK TITLE */
    .blink-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: orange;
        animation: blinker 2s linear infinite;
        margin-bottom: 6px;
    }
    @keyframes blinker { 50% { opacity: 0; } }

    /* Labels / text */
    h2, h3, label, p, span, div { color: white !important; font-weight: bold !important; }

    /* Dropdown box (select) */
    div[data-baseweb="select"] > div {
        background-color: #00264d !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] span { color: orange !important; font-size: 18px !important; font-weight: bold !important; }

    /* Text inputs (server-side fallback visuals) */
    .stTextInput>div>div>input {
        background-color: #00264d !important;
        color: orange !important;
        border: 2px solid orange !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Large centered buttons */
    .big-btn-style button {
        background-color: #ff8c00 !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
        margin: 6px !important;
    }
    .big-btn-style button:hover { background-color: #ffa733 !important; border: 2px solid yellow !important; }

    /* Make the dataframe area more readable */
    .stDataFrame table { color: black !important; background-color: white !important; }

    /* Small helper text */
    .hint { color: #ffd699 !important; font-weight: bold; margin-top: 6px; }

</style>
""", unsafe_allow_html=True)

# -------------------------
# Blinking centered title
# -------------------------
st.markdown("<div class='blink-title'>திருப்பூர் மாவட்டம் வாக்காளர் விபரம் 2002</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center' class='hint'>Type in English — it will convert to Tamil automatically. Then press Search.</div>", unsafe_allow_html=True)

# -------------------------
# AC Map
# -------------------------
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

# Build the UI inside an HTML component so we can attach Google Transliteration to the textboxes
# The component will postMessage back a JSON with {ac, fm, rln, action}
component_html = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {{ background-color: transparent; color: white; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; }}
      .container {{ width:100%; display:flex; justify-content:center; align-items:center; flex-direction:column; gap:8px; }}
      .row {{ display:flex; gap:12px; align-items:center; justify-content:center; }}
      select, input {{
         background-color: #00264d; color: orange; border: 2px solid orange; border-radius:6px; padding:10px 12px;
         font-size:18px; font-weight:bold;
      }}
      .big-btn {{ display:flex; gap:12px; align-items:center; justify-content:center; margin-top:8px; }}
      button {{
         background-color:#ff8c00; color:black; font-weight:bold; font-size:20px; padding:12px 36px; border-radius:8px; border:2px solid white;
      }}
      button#reset {{ background-color: transparent; color: orange; border: 2px solid orange; }}
      .note {{ color:#ffd699; font-weight:bold; }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="row">
        <label for="ac" style="color:white; font-weight:bold; margin-right:6px;">AC தேர்வு</label>
        <select id="ac" name="ac">
            {''.join([f'<option value="{k}">{k}</option>' for k in ac_map.keys()])}
        </select>
      </div>

      <div class="row">
        <input id="fm" placeholder="FM_NAME_V2 (type in English → converts to Tamil)" style="width:540px;" />
      </div>

      <div class="row">
        <input id="rln" placeholder="RLN_FM_NM_V2 (type in English → converts to Tamil)" style="width:540px;" />
      </div>

      <div class="big-btn">
        <button id="search">Search</button>
        <button id="reset">Reset</button>
      </div>

      <div class="note">At least FM or RLN must be filled before Search (FM or RLN or both allowed).</div>
    </div>

    <!-- Load Google Transliteration API -->
    <script src="https://www.google.com/jsapi"></script>
    <script>
      // Ensure google is loaded and then initialize transliteration
      function initTransliteration() {{
        if (!window.google || !google.load) {{
          console.warn('Google jsapi not loaded');
          return;
        }}
        google.load("elements", "1", {{packages: "transliteration"}});

        google.setOnLoadCallback(function() {{
          var options = {{
            sourceLanguage: google.elements.transliteration.LanguageCode.ENGLISH,
            destinationLanguage: [google.elements.transliteration.LanguageCode.TAMIL],
            transliterationEnabled: true
          }};

          var control = new google.elements.transliteration.TransliterationControl(options);

          // Enable transliteration on the two inputs
          control.makeTransliteratable(['fm', 'rln']);

          // Optional: make space trigger conversion immediately (works by default with control)
          // control.crossover? (the API handles it)
        }});
      }}

      // Call initialization after small delay to allow jsapi to load
      initTransliteration();

      // Post message helpers
      function postAction(action) {{
        const payload = {{
          action: action,
          ac: document.getElementById('ac').value,
          fm: document.getElementById('fm').value,
          rln: document.getElementById('rln').value
        }};
        // send to Streamlit
        window.parent.postMessage({{ "streamlitMessage": JSON.stringify(payload) }}, "*");
      }}

      document.getElementById('search').addEventListener('click', function(e) {{
        postAction('search');
      }});

      document.getElementById('reset').addEventListener('click', function(e) {{
        document.getElementById('fm').value = '';
        document.getElementById('rln').value = '';
        postAction('reset');
      }});
    </script>
  </body>
</html>
"""

# The component will return the last posted message as a string (when user clicks Search/Reset)
# We set a fairly large height to accommodate the controls
returned = components_html(component_html, height=360, scrolling=True)

# returned will be None until the user clicks a button in the component.
# After a click, Streamlit receives the posted message as a string like: '{"action":"search", "ac":"102-AVN", "fm":"...","rln":"..."}'
payload = None
if returned:
    try:
        # The component posts window.parent.postMessage({ "streamlitMessage": JSON.stringify(payload) }, "*")
        # Streamlit returns the outer object; parse to get inner JSON string then load it
        # Some Streamlit versions return the raw string; handle both.
        if isinstance(returned, dict) and 'streamlitMessage' in returned:
            payload = json.loads(returned['streamlitMessage'])
        elif isinstance(returned, str):
            # sometimes the component returns the inner JSON string directly
            payload = json.loads(returned)
        else:
            # try to convert dict->json->dict
            payload = returned
    except Exception as e:
        st.error(f"Failed to parse component message: {e}")
        payload = None

# -------------------------
# If payload exists -> handle actions: search / reset
# -------------------------
if payload:
    action = payload.get('action')
    ac_selected = payload.get('ac')
    fm_input = payload.get('fm', '').strip()
    rln_input = payload.get('rln', '').strip()

    # Map AC code to filename
    ac_map_reverse = ac_map  # same mapping used in HTML
    csv_key = ac_map_reverse.get(ac_selected)

    # Attempt to locate CSV
    df = None
    if csv_key:
        csv_path = os.path.join("data", f"{csv_key}.csv")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
            except Exception as e:
                st.error(f"Failed to read CSV {csv_path}: {e}")
        else:
            st.error("CSV கிடைக்கவில்லை! (Check data folder and filenames)")
    else:
        st.error("Invalid AC selected")

    # If reset -> just re-render inputs cleared (no search)
    if action == 'reset':
        st.success("Form reset.")
    elif action == 'search':
        # Validation: require at least FM or RLN (first three cases allowed)
        if not fm_input and not rln_input:
            st.warning("தயவு செய்து FM அல்லது RLN பாராமீட்டரில் ஒன்றை நிரப்பவும் (அல்லது இரண்டும்).")
        else:
            # perform exact-match search (case-insensitive trimmed) using the same find_col helper behavior
            def find_col(df_local, name):
                name = name.lower()
                for col in df_local.columns:
                    if col.lower() == name:
                        return col
                for col in df_local.columns:
                    if name in col.lower():
                        return col
                return None

            if df is None:
                st.stop()

            fm_col = find_col(df, "FM_NAME_V2")
            rln_col = find_col(df, "RLN_FM_NM_V2")

            result = df.copy()

            # BOTH
            if fm_input and rln_input and fm_col and rln_col:
                result = result[
                    (result[fm_col].astype(str).str.strip().str.lower() == fm_input.strip().lower()) &
                    (result[rln_col].astype(str).str.strip().str.lower() == rln_input.strip().lower())
                ]
            # FM only
            elif fm_input and fm_col:
                result = result[
                    result[fm_col].astype(str).str.strip().str.lower() == fm_input.strip().lower()
                ]
            # RLN only
            elif rln_input and rln_col:
                result = result[
                    result[rln_col].astype(str).str.strip().str.lower() == rln_input.strip().lower()
                ]
            else:
                # If column not found or inputs invalid
                if not fm_col and not rln_col:
                    st.error("FM and RLN columns not found in CSV.")
                    st.stop()
                else:
                    st.info("No matches found or search could not be completed.")

            # Show results
            st.markdown(f"#### Search results for AC: **{ac_selected}**  (rows: {len(result)})")
            st.dataframe(result, use_container_width=True)

# If nothing posted yet, show instructions below the component
if not returned:
    st.info("Type in English in the boxes above. They will convert to Tamil as you type (client-side). Then click **Search**.")
