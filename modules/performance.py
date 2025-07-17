# modules/performance.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import load_validator_data

def render():
    st.title("🚀 Validator Performance")
    st.markdown("This section evaluates validator performance based on credits, voting activity, and estimated rewards.")

    data = load_validator_data()
    if not data:
        st.warning("No data found.")
        return

    df = pd.DataFrame(data)

    # KPIs: Last Vote
    max_slot = df["last_vote"].max()
    validators_at_max = df[df["last_vote"] == max_slot].shape[0]
    total_validators = len(df)
    percent_up_to_date = validators_at_max / total_validators * 100

    st.subheader("Key Voting Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🧑‍💻 Total Validators", total_validators)
    col2.metric("⏱️ Latest Slot (Last Vote)", max_slot)
    col3.metric("✅ Up-to-date Validators", f"{percent_up_to_date:.1f}%")

    # Scatterplot: Last Vote vs. Credits
    st.subheader("🔍 Last Vote vs. Credits")
    fig1 = px.scatter(
        df,
        x="last_vote",
        y="credits",
        hover_name="validator_name",
        title="Last Vote Slot vs. Credits",
        labels={"last_vote": "Last Vote Slot", "credits": "Credits"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Barplot: Anzahl Validatoren pro LastVote
    st.subheader("📊 Distribution of Last Vote Slots")
    fig2 = px.histogram(
        df,
        x="last_vote",
        nbins=30,
        title="Frequency of Validators by Last Vote Slot",
        labels={"last_vote": "Last Vote Slot", "count": "Number of Validators"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Estimated Earnings
    st.subheader("💰 Estimated Earnings of Validators")

    SOL_PRICE_USD = 150  # Fixpreis oder dynamisch via API
    credit_reward_factor = 0.000000054  # SOL per Credit per Stake

    df["estimated_rewards_SOL"] = df["credits"] * df["stake"] * credit_reward_factor
    df["estimated_rewards_USD"] = df["estimated_rewards_SOL"] * SOL_PRICE_USD

    top_earnings = df.sort_values("estimated_rewards_USD", ascending=False).head(20)

    fig3 = px.bar(
        top_earnings,
        x="validator_name",
        y="estimated_rewards_USD",
        title="Top 20 Validators by Estimated Rewards (USD)",
        labels={"validator_name": "Validator", "estimated_rewards_USD": "Estimated Rewards (USD)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Performance Table
    st.subheader("📋 Performance Table")
    st.dataframe(
        df[["validator_name", "stake", "credits", "last_vote", "estimated_rewards_SOL", "estimated_rewards_USD"]]
        .sort_values(by="estimated_rewards_USD", ascending=False),
        use_container_width=True
    )
