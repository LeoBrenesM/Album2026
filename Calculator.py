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
    fwcTier1 = st.number_input("FWC 03-08, 17, 18", 0, 999, 0)
    fwcTier2 = st.number_input("FWC 01,02,04,06,07,08, [09-16],19", 0, 999, 0)
    tier1 = st.number_input("Lamine, Julián, Raphinha, Vinicius", 0, 999, 0)
    tier2 = st.number_input("Mbappé, Modric, Haaland, Bellingham", 0, 999, 0)
    tier3 = st.number_input("Messi / CR7", 0, 999, 0)

    total_figuritas = (normales + equipos + escudos + 
                       fwc00 + fwcTier1 + fwcTier2 + 
                       tier1 + tier2 + tier3)

    ### just an idea
    #elif total_figuritas >= 300:
    #     normales_price = 150

    total = (
        normales * 150 +
        escudos * 500 +
        equipos * 300 +
        fwc00 * 500 +
        fwcTier1 * 2000 +
        fwcTier2 * 500 +
        tier1 * 1500 +
        tier2 * 3000 +
        tier3 * 4000
    )

    if total > 0:

        detalle = pd.DataFrame([
            ["Normales", normales, normales * 150, 150],
            ["Equipos", equipos, equipos * 300, 300],
            ["Escudos", escudos, escudos * 500, 500],
            ["FWC 00", fwc00, fwc00 * 500, 500],
            ["FWC 01,02", fwcTier2, fwcTier2 * 500, 500],
            ["FWC 03-08, 17, 18", fwcTier1, fwcTier1 * 2000, 2000],
            ["Lamine, Julián , Raphinha, Vini", tier1, tier1 * 1500,1500],
            ["Mbappé, Modric, Haaland, Belling", tier2, tier2 * 3000, 3000],
            ["Messi / CR7", tier3, tier3 * 4000, 4000],
        ],
        columns=[
            "Tipo",
            "Cantidad",
            "Subtotal"
            "Precio Unitario",
        ])

        detalle = detalle[detalle["Cantidad"] > 0]

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

        st.metric(
            "Valor total",
            f"₡{total:,}"
        )