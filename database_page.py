import model_page as mp
import sqlite3
import streamlit as st


st.title("Database Page")

prediction = mp.model_prediction

conn_data = sqlite3.connect("data_used_pred.db")

conn_data.execute("""
    CREATE TABLE IF NOT EXISTS data_used_pred (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        continent TEXT,
        year INTEGER,
        gdpPercap REAL,
        pop REAL
    )
""")


conn = sqlite3.connect("predictions.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        life_expectancy_pred REAL
    )
""")
