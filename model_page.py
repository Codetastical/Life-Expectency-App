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

        self.dict_data = []
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

        self.conn_data = sqlite3.connect("data_used_pred.db")
        self.conn = sqlite3.connect("predictions.db")

        if not self.dict_data or not self.model_prediction:
            st.warning("Make a prediction first!")
            return
        # Get the latest stored DataFrame
        df = self.dict_data[-1]

        # Get the first row from that DataFrame
        row = df.iloc[0]

        # Save all input features as ONE SQL record
        self.conn_data.execute(
            """
            INSERT INTO data_used_pred
            (country, continent, year, gdpPercap, pop)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(row["country"]),
                str(row["continent"]),
                int(row["year"]),
                float(row["gdpPercap"]),
                float(row["pop"]),
            ),
        )

        self.conn_data.commit()

        # Extract the numerical model prediction
        prediction = float(self.model_prediction[-1][0])

        self.conn.execute(
            """
            INSERT INTO predictions (life_expectancy_pred)
            VALUES (?)
            """,
            (prediction,),
        )

        self.conn.commit()

        st.success("Prediction saved to SQLite!")

    def delete_prediction(self, rm_idx):

        # rm_idx = self.current_prediction_idx

        with sqlite3.connect("data_used_pred.db") as conn_data:
            result_data = conn_data.execute(
                "DELETE FROM data_used_pred WHERE id = ?", (rm_idx,)
            )

        with sqlite3.connect("predictions.db") as conn:
            result_pred = conn.execute(
                "DELETE FROM predictions WHERE id = ?", (rm_idx,)
            )

        if result_data.rowcount == 0 and result_pred.rowcount == 0:
            st.warning(f"No records found with ID {rm_idx}")
        else:
            st.success(f"Deletion completed for ID {rm_idx}")


if "menu" not in st.session_state:
    st.session_state["menu"] = menu()

Menu = st.session_state["menu"]

if btn:
    Menu.model_predict()

if btn_2:
    Menu.save_prediction()

rm_idx = int(st.number_input("remove this index"))
if btn_3:
    Menu.delete_prediction(rm_idx)
