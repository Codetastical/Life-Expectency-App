import model_page as mp
import sqlite3
import streamlit as st
import pandas as pd

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

df_data_u_pred = pd.read_sql_query("SELECT * FROM data_used_pred", conn_data)
conn_data.close()
df_pred = pd.read_sql_query("SELECT * FROM predictions", conn)
conn.close()

inputed_database = st.button("show_inputed_predict_database")
outputed_database = st.button("show_outputed_predict_database")
if inputed_database:
    st.dataframe(df_data_u_pred)
if outputed_database:
    st.dataframe(df_pred)
