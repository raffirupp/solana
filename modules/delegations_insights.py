# modules/delegations_insights.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import load_validator_data
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def render():
    st.title("📡 Delegation Insights with Clustering")
    st.markdown("""
    This section clusters validators based on their **stake**, **commission**, and **credits (voting activity)**.
    By using machine learning (KMeans clustering), we can identify patterns and categorize validators into distinct groups.
    """)

    data = load_validator_data()
    if not data:
        st.warning("No data found.")
        return

    df = pd.DataFrame(data)

    # Log-transform to reduce skew
    df["log_stake"] = np.log1p(df["stake"])
    df["log_credits"] = np.log1p(df["credits"])

    # Prepare features for clustering
    features = df[["log_stake", "commission", "log_credits"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Apply KMeans clustering
    k = 4
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    st.subheader(f"🔍 Applied KMeans Clustering (k={k})")
    st.markdown("""
    The clustering groups validators based on:
    - **Stake (log-scaled)**: how much capital is delegated
    - **Commission (%)**: fee charged by validator
    - **Credits (log-scaled)**: voting activity metric

    This helps to identify **different validator strategies or profiles** in the network.
    """)

    # Visualize clusters: Stake vs Commission
    fig_cluster = px.scatter(
        df,
        x="stake",
        y="commission",
        color="cluster",
        size="credits",
        hover_name="validator_name",
        title="Clusters of Validators: Stake vs Commission (Bubble size = Credits)",
        labels={"stake": "Stake (SOL)", "commission": "Commission (%)"}
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

    # Cluster Summary
    cluster_summary = df.groupby("cluster").agg({
        "stake": "mean",
        "commission": "mean",
        "credits": "mean",
        "validator_name": "count"
    }).rename(columns={"validator_name": "Number of Validators"}).reset_index()

    st.subheader("📊 Cluster Summary Statistics")
    st.dataframe(cluster_summary)

    st.markdown("""
    ### 🧩 **Interpretation of Clusters**
    - **Cluster 0**: High Stake, Low Commission, High Credits – **top-tier performant validators**
    - **Cluster 1**: Medium Stake, Moderate Commission, Moderate Credits – **balanced validators**
    - **Cluster 2**: Low Stake, Low to Medium Commission, Low Credits – **smaller but cheaper validators**
    - **Cluster 3**: Low Stake, High Commission, Very Low Credits – **potentially inactive or low-performing**

    These clusters can help delegators decide where to delegate based on their preferences for fees, validator activity, and size.
    """)

    # Full Table with clusters
    with st.expander("📋 Show Full Delegation Table with Cluster Assignment"):
        st.dataframe(df[["validator_name", "stake", "commission", "credits", "cluster"]])
