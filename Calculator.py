import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.subheader("Calculadora de intercambio")

normales = st.number_input("Normales", 0, 999, 0)
escudos = st.number_input("Escudos", 0, 999, 0)
equipos = st.number_input("Equipos", 0, 999, 0)
fwc = st.number_input("FWC", 0, 999, 0)

tier3 = st.number_input("Messi / CR7", 0, 999, 0)
tier2 = st.number_input("Lamine", 0, 999, 0)
tier1 = st.number_input("Mbappe", 0, 999, 0)

total = (
    normales * 1 +
    escudos * 2 +
    equipos * 3 +
    fwc * 4 +
    tier3 * 5 +
    tier2 * 7 +
    tier1 * 10
)

st.metric(
    "Valor total estimado",
    total
)