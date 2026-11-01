import streamlit as st
import joblib
import pandas as pd
import sqlite3

# Load the trained neural network
model = joblib.load("life_expectancy_nn.joblib")
model

st.title("Model Page")
param_1 = st.text_input("country?:").lower()
param_2 = st.text_input("continnent?: ").lower()
param_3 = st.number_input("year?: ")
param_4 = st.number_input("gdpPercap?: ")
param_5 = st.number_input("population?: ")

btn = st.button("enter parameters", width=1.0)
btn_2 = st.button("save prediction to .db", width=0.5)
btn_3 = st.button("remove prediction from .db", width=0.5)
model_prediction = []
current_prediction_idx = 0
conn = sqlite3.connect("predictions.db")


class menu:
    def __init__(self, choice: str):
        print("""Choice: 1-3
                 1: Predict with model
                 2: Save Model Prediction in  database
                 3: Delete Model Prediction           
                            """)

    def model_predict():
        if btn:
            data = pd.DataFrame(
                [
                    {
                        "country": param_1,
                        "continent": param_2,
                        "year": param_3,
                        "gdpPercap": param_4,
                        "pop": param_5,
                    }
                ]
            )
            model_prediction.append(model(data))
            current_prediction_idx += 1
            st.write_stream(model(data))

    def save_prediction():
        conn.execute(
            f"INSERT INTO predictions (life_expectancy) VALUES (?)",
            ("Sweden", 2007, 82.4),
        )

    def save_prediction():
        pass
