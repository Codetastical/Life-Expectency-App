import streamlit as st
import joblib
import pandas as pd

# Load the trained neural network
model = joblib.load("life_expectancy_nn.joblib")
model

st.title("Model Page")
param_1 = st.text_input("country?:").lower()
param_2 = st.text_input("continnent?: ").lower()
param_3 = st.number_input("year?: ")
param_4 = st.number_input("gdpPercap?: ")
param_5 = st.number_input("population?: ")

btn = st.button("enter parameters")
model_prediction = []


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
            st.write_stream(model(data))

    def save_prediction():
        pass
