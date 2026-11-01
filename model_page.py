import streamlit as st
import joblib
import pandas as pd
import sqlite3

# Load the trained neural network
model = joblib.load("life_expectancy_nn.joblib")


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

        self.conn_data = sqlite3.connect("data_used_pred.db")
        self.conn = sqlite3.connect("predictions.db")

        self.dict_data = []
        # self.true_data = []
        self.dict_data_idx = 0

        self.model_prediction = []
        self.current_prediction_idx = 0

    def model_predict(self):
        self.data = pd.DataFrame(
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
        self.dict_data.append(self.data)
        self.dict_data_idx += 1
        self.model_prediction.append(model.predict(self.data))
        self.current_prediction_idx += 1
        st.write(
            f"predicted lifespan: {model.predict(self.data)}, idx: {self.dict_data}"
        )

    def save_prediction(self):
        st.write(self.dict_data)
        if btn_2:
            for dic_item in self.dict_data:
                for df in dic_item:
                    for name in df.columns:
                        self.conn_data.execute(
                            f"INSERT INTO predictions ({name}) VALUES (?)",
                            (df[name]),
                        )
            self.conn_data.commit()
            self.conn.execute(
                "INSERT INTO predictions (life_expectancy_pred) VALUES (?)",
                (self.model_prediction[self.current_prediction_idx - 1],),
            )
            self.conn.commit()

            st.write(f"Saved Prediction: {self.dict_data} to .db")

    def delete_prediction(self):
        if btn_3:
            print(f"All index choices 0-{len(self.model_prediction)}")
            rm_idx = int(
                st.number_input("Input what idx do you want to remove from data row?")
            )
            self.conn_data.execute("DELTE FROM data_used_pred WHERE id = ?", (rm_idx,))
            self.conn.execute("DELETE FROM predictions WHERE id = ?", (rm_idx,))
            self.conn.commit()

            st.write("Deleted Prediction from .db")


if "menu" not in st.session_state:
    st.session_state["menu"] = menu()

Menu = st.session_state["menu"]

if btn:
    Menu.model_predict()

if btn_2:
    Menu.save_prediction()
if btn_3:
    Menu.delete_prediction()
