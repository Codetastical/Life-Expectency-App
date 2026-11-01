import streamlit as st
import joblib
import pandas as pd
import sqlite3

# Load the trained neural network
model = joblib.load("life_expectancy_nn.joblib")
conn_data = sqlite3.connect("data_used_pred.db")
conn = sqlite3.connect("predictions.db")

st.title("Model Page")
param_1 = st.text_input("country?:")
param_2 = st.text_input("continnent?: ")
param_3 = int(st.number_input("year?: "))
param_4 = st.number_input("gdpPercap?: ")
param_5 = st.number_input("population?: ")

btn = st.button("enter parameters", width="stretch")
btn_2 = st.button("save prediction to .db", width="stretch")
btn_3 = st.button("remove prediction from .db", width="stretch", icon_position="right")


class menu:
    def __init__(self):
        self.dict_data = []
        self.dict_data_idx = 0

        self.model_prediction = []
        self.current_prediction_idx = 0

    def model_predict(self):
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
            self.dict_data.append(data)
            self.dict_data_idx += 1
            self.model_prediction.append(model.predict(data))
            self.current_prediction_idx += 1
            st.write(model.predict(data))

    def save_prediction(self):
        with btn_2:
            for dic_item in self.dict_data[self.dict_data_idx]:
                conn_data.execute(
                    f"INSERT INTO predictions ({dic_item.key}) VALUES (?)",
                    (f"{dic_item.item}"),
                )
            conn_data.commit()
            conn.execute(
                "INSERT INTO predictions (life_expectancy_pred) VALUES (?)",
                (f"{self.model_prediction[self.current_prediction_idx - 1]}"),
            )
            conn.commit()

            st.write("Saved Prediction! from .db")

    def delete_prediction(self):
        if btn_3:
            print(f"All index choices 0-{len(self.model_prediction)}")
            rm_idx = int(input("Input what idx do you want to remove from data row?"))
            conn_data.execute("DELTE FROM data_used_pred WHERE id = ?", (rm_idx,))
            conn.execute("DELETE FROM predictions WHERE id = ?", (rm_idx,))
            conn.commit()

            st.write("Deleted Prediction from .db")


Menu = menu()

if btn:
    Menu.model_predict()

if btn_2:
    Menu
