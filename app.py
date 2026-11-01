import streamlit as st
import database_page

pg = st.navigation(["model_page.py", "database_page.py"])
pg.run()
