# modules/overview.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import load_validator_data

def render():
    st.title("🏠 Overview")
    st.markdown("Welcome to the Solana Validator Dashboard – powered by live API data.")

    data = load_validator_data()
    if not data:
        st.warning("No data received from API.")
        return

    df = pd.DataFrame(data)

    # KPIs
    total_validators = len(df)
    total_stake = df["stake"].sum()
    avg_stake = df["stake"].mean()
    max_stake = df["stake"].max()

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🧑‍💻 Validators", total_validators)
    col2.metric("💰 Total Stake (SOL)", f"{total_stake:,.2f}")
    col3.metric("📊 Average Stake (SOL)", f"{avg_stake:,.2f}")
    col4.metric("🏆 Max Stake (SOL)", f"{max_stake:,.2f}")

    # Suche
    search_term = st.text_input("🔎 Search for Validator by Name:")
    if search_term:
        df = df[df['validator_name'].str.contains(search_term, case=False, na=False)]

    # Stake-Verteilung bis 3M SOL
    st.subheader("Distribution of Stake (SOL) - Focused View (<= 3M SOL)")
    df_stake_filtered = df[df['stake'] <= 3_000_000]
    fig_stake = px.histogram(
        df_stake_filtered,
        x='stake',
        nbins=int(3_000_000 / 10_000),  # 10k Granularität
        title="Stake Distribution across Validators (up to 3M SOL)",
        labels={"stake": "Stake (SOL)"}
    )
    st.plotly_chart(fig_stake, use_container_width=True)

    # Stake Boxplot bis 1M SOL
    st.subheader("Stake Distribution - Boxplot View (<= 1M SOL)")
    df_stake_box = df_stake_filtered[df_stake_filtered['stake'] <= 1_000_000]
    stake_count_box = len(df_stake_box)

    fig_stake_box = px.box(
        df_stake_box,
        y='stake',
        title=f"Stake Boxplot (up to 1M SOL) - {stake_count_box} Validators",
        labels={"stake": "Stake (SOL)"}
    )
    st.plotly_chart(fig_stake_box, use_container_width=True)

    # Credits-Verteilung bis 700M Credits
    st.subheader("Distribution of Credits - Focused View (<= 700M)")
    df_credits_filtered = df[df['credits'] <= 700_000_000]
    fig_credits = px.histogram(
        df_credits_filtered,
        x='credits',
        nbins=int(700_000_000 / 50_000_000),  # ca. 14 Bins à 50 Mio
        title="Credits Distribution across Validators (up to 700M Credits)",
        labels={"credits": "Credits"}
    )
    st.plotly_chart(fig_credits, use_container_width=True)

    # Credits Boxplot
    st.subheader("Credits Distribution - Boxplot View")
    credits_count = len(df_credits_filtered)
    fig_credits_box = px.box(
        df_credits_filtered,
        y='credits',
        title=f"Credits Boxplot (up to 700M) - {credits_count} Validators",
        labels={"credits": "Credits"}
    )
    st.plotly_chart(fig_credits_box, use_container_width=True)

    # Tabelle
    st.subheader("🔎 Validator List")
    st.dataframe(df.sort_values("stake", ascending=False), use_container_width=True)
