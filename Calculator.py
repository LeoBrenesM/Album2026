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
    elif total_figuritas >= 100:
        normales_price = 125

    ### just an idea
    #elif total_figuritas >= 300:
    #     normales_price = 150

    total = (
        normales * 1 +
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

    st.metric(
        "Valor total estimado",
        total
    )