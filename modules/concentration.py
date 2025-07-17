# modules/concentration.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import load_validator_data
from utils.metrics import gini, top_n_share
from scipy.stats import pearsonr

def render():
    st.title("📈 Stake & Credit Concentration")
    st.markdown("This section explores the concentration of stake and credits across validators, and examines their correlation.")

    data = load_validator_data()
    if not data:
        st.warning("No data found.")
        return

    df = pd.DataFrame(data)

    # --- Section 1: Stake Concentration ---
    st.subheader("1️⃣ Stake Concentration")

    gini_stake = gini(df["stake"])
    top10_stake_share = top_n_share(df["stake"], n=10)

    st.metric("🔹 Gini Coefficient (Stake)", f"{gini_stake:.3f}")
    st.caption(
        f"A Gini coefficient of {gini_stake:.3f} indicates a **high concentration of stake**. "
        "This means that a small number of validators hold a large portion of the total stake, "
        "potentially raising concerns about capital centralization in the network."
    )

    st.metric("🔸 Top 10 Share (Stake)", f"{top10_stake_share:.1%}")
    st.caption(
        f"The top 10 validators collectively hold **{top10_stake_share:.1%} of the total stake**, "
        "which further highlights how concentrated the capital power is."
    )

    st.markdown("### 🏆 Top 30 Validators by Stake")
    fig_stake = px.bar(
        df.sort_values(by="stake", ascending=False).head(30),
        x="validator_name",
        y="stake",
        title="Top 30 Validators by Stake (SOL)",
        labels={"stake": "Stake (SOL)", "validator_name": "Validator"},
    )
    st.plotly_chart(fig_stake, use_container_width=True)

    # --- Section 2: Credit Concentration ---
    st.subheader("2️⃣ Credit Concentration")

    gini_credits = gini(df["credits"])
    top10_credits_share = top_n_share(df["credits"], n=10)

    st.metric("🔹 Gini Coefficient (Credits)", f"{gini_credits:.3f}")
    st.caption(
        f"A Gini coefficient of {gini_credits:.3f} suggests that **credits (voting activity)** "
        "are more evenly distributed compared to stake. This indicates that validators with smaller stakes "
        "still actively contribute to network consensus by voting."
    )

    st.metric("🔸 Top 10 Share (Credits)", f"{top10_credits_share:.1%}")
    st.caption(
        f"The top 10 validators generate only **{top10_credits_share:.1%} of total credits**, "
        "highlighting a relatively decentralized voting behavior across the network."
    )

    st.markdown("### 🏆 Top 30 Validators by Credits")
    fig_credits = px.bar(
        df.sort_values(by="credits", ascending=False).head(30),
        x="validator_name",
        y="credits",
        title="Top 30 Validators by Credits",
        labels={"credits": "Credits", "validator_name": "Validator"},
    )
    st.plotly_chart(fig_credits, use_container_width=True)

    # --- Section 3: Correlation between Stake and Credits ---
    st.subheader("3️⃣ Correlation between Stake and Credits")

    pearson_r, p_value = pearsonr(df["stake"], df["credits"])
    st.write(f"**Pearson Correlation (r)** between stake and credits: `{pearson_r:.3f}` (p = {p_value:.4f})")

    st.caption(
        f"The correlation between stake and credits is **very weak** (r = {pearson_r:.3f}). "
        "This means that having more stake does not strongly predict having more credits. "
        "Thus, validators with smaller stakes can still accumulate significant credits through active participation."
    )

    fig_corr = px.scatter(
        df,
        x="stake",
        y="credits",
        title="Scatterplot of Stake vs. Credits",
        labels={"stake": "Stake (SOL)", "credits": "Credits"},
        opacity=0.7
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # --- Section 4: Takeaways / Insights ---
    st.markdown("""
    ---
    ### 🧠 **Key Takeaways**
    - **Stake** is highly concentrated among a few validators, as indicated by a high Gini coefficient.
    - **Credits (voting activity)** are more evenly distributed, enabling smaller validators to actively contribute.
    - The **weak correlation between stake and credits** suggests that operational decentralization exists despite capital concentration.
    - This dynamic supports network resilience but also raises questions about **governance and reward fairness**.
    """)
