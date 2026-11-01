import model_page as mp
import sqlite3
import streamlit as st


st.title("Database Page")

prediction = mp.model_prediction

conn_zero = sqlite3.connect("data_used_pred.db")

conn_zero
conn = sqlite3.connect("predictions.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        life_expectancy_pred REAL
    )
""")
