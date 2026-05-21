import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ===== GOOGLE SHEETS AUTH =====

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    #"https://www.googleapis.com/auth/drive.readonly"
]

creds = Credentials.from_service_account_file(
    "fwc2026-Cred.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

# ===== OPEN SHEET =====

#spreadsheet = client.open("Album 2026 FWC")
spreadsheet = client.open_by_key("10H8tULd57u10wKGKxLOTyhh3dwIpBqwnFNhOgmIEW3s")

worksheet = spreadsheet.get_worksheet(0)

# ===== LOAD DATAFRAME =====

data = worksheet.get_all_values()

df = pd.DataFrame(data)

# # ===== CONFIG =====
# file_path = r"C:\Users\lbren\OneDrive\Documents\Documentos\proyectario\Album 2026\Album 2026 FWC.xlsx"
# sheet_name = 0

# # ==================
# df = pd.read_excel(
#     file_path,
#     sheet_name=sheet_name,
#     header=None,
#     engine="openpyxl"
# )

results = []

# ===== USER FILTER =====

print("Opciones de filtro:")
print("1 = Mas de X")
print("2 = Menos de X")
print("3 = Iguales a X")

while True:

    mode = input(
        "\nEscoge una opcion (1/2/3): "
    ).strip()

    if mode in ["1", "2", "3"]:
        break

    print("Opcion invalida. Escoge 1, 2 o 3.")

while True:
    try:
        threshold = int(input("Ingresa la cantidad X: "))
        break
    except:
        print("Ingresa un numero valido.")

# =======================

# Scan ALL columns
for col in range(df.shape[1]):

    country = df.iloc[1, col]

    # Ignore blank columns
    if pd.isna(country):
        continue

    qty_col = col + 1

    if qty_col >= df.shape[1]:
        continue

    for row in range(3, len(df)):

        sticker = df.iloc[row, col]
        qty = df.iloc[row, qty_col]

        # Stop at TOTAL
        if str(sticker).strip().upper() == "TOTAL":
            break

        if pd.isna(sticker):
            continue

        try:
            qty = int(qty)
        except:
            continue

        results.append((country, sticker, qty))

# ===== FILTER FUNCTION =====

def passes_filter(qty):

    if mode == "1":
        return qty > threshold

    elif mode == "2":
        return qty < threshold

    elif mode == "3":
        return qty == threshold

    return False

# ===== PRINT RESULTS =====

filtered_results = [
    (country, sticker, qty)
    for country, sticker, qty in results
    if passes_filter(qty)
]

if not filtered_results:
    print("\nNo se encontraron stickers.")


else:

    
    if mode == "1":
        print(f"\nA continuacion las que tenemos mas de {threshold} postales:")

    elif mode == "2":
        print(f"\nA continuacion las que tenemos menos de {threshold} postales:")

    elif mode == "3":
        print(f"\nA continuacion las que tenemos {threshold} postales:")

    current_country = None
    country_stickers = []

    for country, sticker, qty in filtered_results:

        if country != current_country:

            # Print previous country
            if current_country is not None:
                print(", ".join(country_stickers))

            # Start new country
            current_country = country
            country_stickers = []

            print(f"\n{country}:")

        country_stickers.append(f"{sticker}")

    # Print last country
    if country_stickers:
        print(", ".join(country_stickers))