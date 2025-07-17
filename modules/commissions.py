# modules/commissions.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.api import load_validator_data
from scipy.stats import pearsonr

def render():
    st.title("💸 Commission Analysis")
    st.markdown("This section provides insights into validator commission rates, their distribution, and how they relate to voting activity (credits).")

    data = load_validator_data()
    if not data:
        st.warning("No data found.")
        return

    df = pd.DataFrame(data)

    # --- KPI-Board ---
    avg_commission = df["commission"].mean()
    median_commission = df["commission"].median()
    min_commission = df["commission"].min()
    max_commission = df["commission"].max()

    st.subheader("Key Metrics on Commission Rates")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Average Commission (%)", f"{avg_commission:.2f}")
    col2.metric("📈 Median Commission (%)", f"{median_commission:.2f}")
    col3.metric("🔽 Minimum Commission (%)", f"{min_commission}")
    col4.metric("🔼 Maximum Commission (%)", f"{max_commission}")

    # --- Commission Rate Distribution: Scatterplot ---
    st.subheader("Commission Rate Distribution - All Validators")
    df_sorted = df.sort_values(by="commission")
    fig_scatter = px.scatter(
        df_sorted,
        x=df_sorted.index,
        y="commission",
        title="Scatterplot of Commission Rates across Validators",
        labels={"commission": "Commission (%)", "index": "Validator Index"},
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Deep Dive: Commission < 10% ---
    st.subheader("🔍 Deep Dive: Commission Rates under 10%")
    df_under_10 = df[df["commission"] < 10]

    if len(df_under_10) > 0:
        fig_deepdive = px.box(
            df_under_10,
            y="commission",
            title=f"Boxplot of Commission Rates under 10% ({len(df_under_10)} Validators)",
            labels={"commission": "Commission (%)"}
        )
        st.plotly_chart(fig_deepdive, use_container_width=True)
    else:
        st.info("No validators with commission rates under 10% found.")

    # --- Correlation between Commission and Credits ---
    st.subheader("🔗 Correlation between Commission and Credits")

    pearson_r, p_value = pearsonr(df["commission"], df["credits"])
    st.write(f"**Pearson Correlation (r)** between commission and credits: `{pearson_r:.3f}` (p = {p_value:.4f})")

    st.caption(
        f"This correlation measures how commission rates relate to the number of credits (voting activity). "
        f"A low correlation would suggest that commission policies do not significantly impact validator activity levels."
    )

    fig_corr = px.scatter(
        df,
        x="commission",
        y="credits",
        title="Scatterplot of Commission vs. Credits",
        labels={"commission": "Commission (%)", "credits": "Credits"},
        opacity=0.7
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # --- Commission Table ---
    st.subheader("📋 Commission Overview Table")
    st.dataframe(
        df[["validator_name", "stake", "commission", "credits"]].sort_values(by="commission"),
        use_container_width=True
    )
