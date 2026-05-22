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

show_qty = st.sidebar.checkbox(
    "Mostrar cantidades",
    value=False
)

show_normals = st.sidebar.checkbox(
    "Mostrar jugadores",
    value=True
)

show_shields = st.sidebar.checkbox(
    "Mostrar escudos",
    value=True
)

show_teams = st.sidebar.checkbox(
    "Mostrar equipos",
    value=True
)

results = []
qty_shown = 0

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

def players_filter(sticker):
    sticker = str(sticker)
    if show_normals:
        return True
    elif sticker.startswith("FW"):
        True
    elif sticker.endswith(" 1"):
        True
    return sticker.endswith(" 13")

def shields_filter(sticker):
    sticker = str(sticker)
    if show_shields:
        return True
    if sticker.startswith("FW"):
        True
    return not sticker.endswith(" 1")

def teams_filter(sticker):
    sticker = str(sticker)
    if show_teams:
        return True
    if sticker.startswith("FW"):
        True
    return not sticker.endswith(" 13")

filtered_results = [
    (country, sticker, qty)
    for country, sticker, qty in results
    if passes_filter(qty)
        if shields_filter(sticker)
        if teams_filter(sticker)
]

# ===== DISPLAY =====

output_text = ""

current_country = None
country_stickers = []

for country, sticker, qty in filtered_results:
    qty_shown += 1
    if country != current_country:

        # Print previous country
        if current_country is not None:
            output_text += ", ".join(country_stickers) + "\n\n"

        # Start new country
        current_country = country
        country_stickers = []

        output_text += f"{country}:\n"

    if show_qty:
        country_stickers.append(f"{sticker} ({qty})")
    else:
        country_stickers.append(f"{sticker}")

# Print last country
if country_stickers:
    output_text += ", ".join(country_stickers)
    #qty_shown += 1

# ===== SHOW TEXT =====

if filtered_results:
    if mode == "Mas de X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con mas de {threshold} postal(es) cada uno.\n\n{output_text}"
        )

    elif mode == "Menos de X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con menos de {threshold} postal(es) cada uno.\n\n{output_text}"
        )

    elif mode == "Igual a X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con exactamente {threshold} postal(es) cada uno.\n\n{output_text}"
        )

    st.code(output_text)

else:

    if mode == "Mas de X":
        output_text = (
            f"No hay stickers con mas de {threshold} copias."
        )

    elif mode == "Menos de X":
        output_text = (
            f"No hay stickers con menos de {threshold} copias."
        )

    elif mode == "Igual a X":
        output_text = (
            f"No hay stickers con exactamente {threshold} copias."
        )

    st.warning(output_text)