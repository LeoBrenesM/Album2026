import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def show_calculator():
    st.subheader("Calculadora de intercambio")

    normales = st.number_input("Normales", 0, 999, 0)
    equipos = st.number_input("Equipos", 0, 999, 0)
    escudos = st.number_input("Escudos", 0, 999, 0)
    fwc00 = st.number_input("FWC00", 0, 999, 0)
    fwcTier1 = st.number_input("FWC05 / FWC03 (Bola y mascota)", 0, 999, 0)
    fwcTier2 = st.number_input("FWC 01,02,04,06,07,08", 0, 999, 0)
    fwcTier3 = st.number_input("FWC Campeones 09-19", 0, 999, 0)
    tier1 = st.number_input("Dembele, Haaland, Julián Álvarez, Modric, Raphinha, Vinicius, Michael Olise, Bellingham", 0, 999, 0)
    tier2 = st.number_input("Mbappe / Lamine", 0, 999, 0)
    tier3 = st.number_input("Messi / CR7", 0, 999, 0)

    total_figuritas = (normales + equipos + escudos + 
                       fwc00 + fwcTier1 + fwcTier2 + fwcTier3+
                       tier1 + tier2 + tier3)

    normales_price = 150
    t2_price = 300

    if total_figuritas >= 50:
        normales_price = 140
    if total_figuritas >= 100:
        normales_price = 125

    ### just an idea
    #elif total_figuritas >= 300:
    #     normales_price = 150

    total = (
        normales * normales_price +
        escudos * 500 +
        equipos * 200 +
        fwc00 * 1500 +
        fwcTier1 * 1000 +
        fwcTier2 * 500 +
        fwcTier3 * 1000 +
        tier1 * 1500 +
        tier2 * 3000 +
        tier3 * 4000
    )

    if total > 0:

        detalle = pd.DataFrame([
            ["Normales", normales, normales_price, normales * normales_price],
            ["Equipos", equipos, 200, equipos * 200],
            ["Escudos", escudos, 500, escudos * 500],
            ["FWC 00", fwc00, 1500, fwc00 * 1500],
            ["FWC 03 / FWC 05", fwcTier1, 1000, fwcTier1 * 1000],
            ["FWC 01,02,04,06,07,08", fwcTier2, 500, fwcTier2 * 500],
            ["FWC Campeones [09-17]", fwcTier3, 1000, fwcTier3 * 1000],
            ["Tier 1", tier1, 1500, tier1 * 1500],
            ["Mbappé / Lamine", tier2, 3000, tier2 * 3000],
            ["Messi / CR7", tier3, 4000, tier3 * 4000],
        ],
        columns=[
            "Tipo",
            "Cantidad",
            "Precio Unitario",
            "Subtotal"
        ])

        st.dataframe(
            detalle,
            use_container_width=True,
            hide_index=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"Total de postales: {total_figuritas}"
            )

        with col2:
            st.info(
                f"Precio normales: ₡{normales_price:,}"
            )

        st.metric(
            "Valor total estimado",
            f"₡{total:,}"
        )