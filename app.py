import streamlit as st
from Inventory import show_inventory
from Calculator import show_calculator

st.set_page_config(
    page_title="Figuritas 2026",
    layout="wide"
)

st.title("Figuritas 2026")

page = st.sidebar.radio(
    "Selecciona una seccion",
    [
        "Inventario",
        "Calculadora"
    ]
)

if page == "Inventario":
    show_inventory()

elif page == "Calculadora":
    show_calculator()