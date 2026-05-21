import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ===== PAGE =====

st.title("Album Panini 2026")

# ===== GOOGLE AUTH =====

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

# ===== OPEN SHEET =====

spreadsheet = client.open_by_key(
    "10H8tULd57u10wKGKxLOTyhh3dwIpBqwnFNhOgmIEW3s"
)

worksheet = spreadsheet.get_worksheet(0)

data = worksheet.get_all_values()

df = pd.DataFrame(data)

# ===== FILTERS =====

st.sidebar.header("Filtros")

mode = st.sidebar.selectbox(
    "Tipo de filtro",
    [
        "Mas de X",
        "Menos de X",
        "Igual a X"
    ]
)

threshold = st.sidebar.number_input(
    "Cantidad X",
    min_value=0,
    value=2
)

results = []

# ===== PROCESS DATA =====

for col in range(df.shape[1]):

    country = df.iloc[1, col]

    if pd.isna(country) or country == "":
        continue

    qty_col = col + 1

    if qty_col >= df.shape[1]:
        continue

    for row in range(3, len(df)):

        sticker = df.iloc[row, col]
        qty = df.iloc[row, qty_col]

        if str(sticker).strip().upper() == "TOTAL":
            break

        if pd.isna(sticker) or sticker == "":
            continue

        try:
            qty = int(qty)
        except:
            continue

        results.append((country, sticker, qty))

# ===== FILTER =====

def passes_filter(qty):

    if mode == "Mas de X":
        return qty > threshold

    elif mode == "Menos de X":
        return qty < threshold

    elif mode == "Igual a X":
        return qty == threshold

    return False

filtered_results = [
    (country, sticker, qty)
    for country, sticker, qty in results
    if passes_filter(qty)
]

# ===== DISPLAY =====

output_text = ""

current_country = None
country_stickers = []

if not filtered_results:

    if mode == "1":
        output_text = (
            f"No hay stickers con mas de {threshold} copias."
        )

    elif mode == "2":
        output_text = (
            f"No hay stickers con menos de {threshold} copias."
        )

    elif mode == "3":
        output_text = (
            f"No hay stickers con exactamente {threshold} copias."
        )

    st.warning(output_text)
    
for country, sticker, qty in filtered_results:

    if country != current_country:

        # Print previous country
        if current_country is not None:
            output_text += ", ".join(country_stickers) + "\n\n"

        # Start new country
        current_country = country
        country_stickers = []

        output_text += f"{country}:\n"

    country_stickers.append(f"{sticker}")

# Print last country
if country_stickers:
    output_text += ", ".join(country_stickers)

# ===== SHOW TEXT =====

st.code(output_text)