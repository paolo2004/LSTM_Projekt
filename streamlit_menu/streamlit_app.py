import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
#--- PAGE SETUP ---
about_page = st.Page(
    page="view/about_me.py",
    title="About Me",
    icon="😁",
    default=True
)
project_1_page = st.Page(
    page="view/about_the_app.py",
    title="About the App",
    icon="👌"
)
project_2_page = st.Page(
    page="view/stock_description.py",
    title="Infos about a stock",
    icon="😎"
)
project_3_page = st.Page(
    page="view/recent_news.py",
    title="Recent News",
    icon="🆕"
)
project_4_page = st.Page(
    page="view/future_ipo.py",
    title="Upcoming IPO",
    icon="ℹ️"
)
project_5_page = st.Page(
    page="view/price_predictor.py",
    title="Price Predictor",
    icon="📈"
)

# ---NAVIGATION SETUP (WITHOUT SECTIONS)---
#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])


# ---NAVIGATION SETUP (WITH SECTIONS)---
pg = st.navigation(
    {
        "Info": [about_page, project_1_page],
        "Stock": [project_2_page, project_3_page, project_4_page, project_5_page],
    }
)

# ---RUN NAVIGATION ---
pg.run()

#Background_color
st.markdown("""
    <style>
    .stApp {
        background-color: aliceBlue;
    }
    </style>
""", unsafe_allow_html=True)


