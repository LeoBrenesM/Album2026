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
TYPE_PLAYERS = "Jugadores"
TYPE_SHIELDS = "Escudos"
TYPE_TEAMS = "Equipos"
TYPE_FW = "FW"

selected_types = st.sidebar.multiselect(
    "Tipos",
    [
        TYPE_PLAYERS,
        TYPE_SHIELDS,
        TYPE_TEAMS,
        TYPE_FW
    ],
    default=[
        TYPE_PLAYERS,
        TYPE_SHIELDS,
        TYPE_TEAMS
    ]
)

results = []
current_group_name = ""

# ===== PROCESS DATA =====

for col in range(df.shape[1]):

    country = df.iloc[1, col]
    group_cell = df.iloc[0, col]

    if pd.notna(group_cell) and group_cell != "":
        current_group_name = group_cell

    group = current_group_name

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

        results.append((group, country, sticker, qty))

# ===== FILTER =====
def passes_filter(qty):

    if mode == "Mas de X":
        return qty > threshold

    elif mode == "Menos de X":
        return qty < threshold

    elif mode == "Igual a X":
        return qty == threshold

    return False

def is_fw(sticker):
    return str(sticker).startswith("FW")

def is_shield(sticker):
    return str(sticker).endswith(" 1")

def is_team(sticker):
    return str(sticker).endswith(" 13")

def is_player(sticker):

    sticker = str(sticker)

    return (
        not is_fw(sticker)
        and not is_shield(sticker)
        and not is_team(sticker)
    )

def should_include_sticker(sticker, qty):

    # ===== QUANTITY =====

    if not passes_filter(qty):
        return False

    # ===== TYPE FILTER =====

    if is_shield(sticker):
        return "Escudos" in selected_types

    if is_team(sticker):
        return "Equipos" in selected_types

    if is_fw(sticker):
        return "FW" in selected_types

    if is_player(sticker):
        return "Jugadores" in selected_types

    return False

filtered_results = [
    (group, country, sticker, qty)
    for group, country, sticker, qty in results
    if should_include_sticker(sticker, qty)
]

# ===== DISPLAY =====

output_text = ""
lines = []

current_country = None
current_group = None
country_stickers = []

for group, country, sticker, qty in filtered_results:
    
    if group != current_group:

        # flush previous country first
        if country_stickers:
            lines.append(", ".join(country_stickers))
            lines.append("")

        current_group = group
        current_country = None
        country_stickers = []

        lines.append(f"## - {group} - ##")
        lines.append("")

    if country != current_country:

        # Print previous country
        if current_country is not None:
            lines.append(", ".join(country_stickers) + "\n\n")

        # Start new country
        current_country = country
        country_stickers = []

        lines.append(f"{country}:\n")

    if show_qty:
        country_stickers.append(f"{sticker} ({qty})")
    else:
        country_stickers.append(f"{sticker}")

# Print last country
if country_stickers:
    lines.append(", ".join(country_stickers))

# ===== SHOW TEXT =====

if filtered_results:
    qty_shown = len(filtered_results)
    if mode == "Mas de X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con mas de {threshold} postal(es) cada uno.\n\n" + "".join(lines)
        )

    elif mode == "Menos de X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con menos de {threshold} postal(es) cada uno.\n\n" + "".join(lines)
        )

    elif mode == "Igual a X":
        output_text = (
            f"Hay {qty_shown} sticker(s) con exactamente {threshold} postal(es) cada uno.\n\n" + "".join(lines)
        )

    st.code(output_text)
    #st.markdown(output_text)

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