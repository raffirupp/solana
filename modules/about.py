import streamlit as st


def render():
    
    st.title("ℹ️ About this Dashboard")

    st.markdown("""
    This dashboard was created as a prototype during the **Data x Chain: Breakout Hackathon 2025**, organized by **Staking Facilities**.

    🧠 **Goal**: Provide transparent, real-time insights into the validator landscape on the [Solana](https://solana.com/) blockchain – tailored for delegators, validators, and curious analysts.

    ### 🔍 Features
    - Stake concentration analysis (Gini coefficient, Top 10 share)
    - Commission distribution overview
    - Performance insights based on credits and vote activity
    - Delegation behavior and cumulative stake visualization
    - Live Solana JSON-RPC integration

    ### ⚒️ Built with
    - Python & [Streamlit](https://streamlit.io)
    - [Solana JSON-RPC](https://docs.solana.com/developing/clients/jsonrpc-api)
    - Open data. No tracking. No wallet required.

    ---

    Made with ❤️ and open data.

    ---
    
    📬 **Contact**: [raffael.ruppert@sciencespo.fr](mailto:raffael.ruppert@sciencespo.fr)
    """)
