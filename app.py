# app.py
import streamlit as st
from modules import (
    overview,
    concentration,
    commissions,
    performance,
    delegations_insights,
    about,
)

# Page config
st.set_page_config(page_title="Solana Validator Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("📊 Solana Validator Dashboard")
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Stake Concentration",
        "Commissions",
        "Performance",
        "Delegation Insights",
        "About",
    ],
)

# Routing to modules
if page == "Overview":
    overview.render()
elif page == "Stake Concentration":
    concentration.render()
elif page == "Commissions":
    commissions.render()
elif page == "Performance":
    performance.render()
elif page == "Delegation Insights":
    delegations_insights.render()
elif page == "About":
    about.render()
