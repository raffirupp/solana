# utils/api.py

import requests
from utils.preprocessing import normalize_validator_data

RPC_URL = "https://api.mainnet-beta.solana.com"

def fetch_vote_accounts():
    """Fetch current validator vote accounts from Solana JSON-RPC."""
    try:
        response = requests.post(
            RPC_URL,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getVoteAccounts"
            }
        )
        response.raise_for_status()
        return response.json()["result"]["current"]
    except Exception as e:
        print(f"[API Error] Could not fetch vote accounts: {e}")
        return []

def load_validator_data():
    """Load and normalize validator data from API."""
    raw_data = fetch_vote_accounts()
    return normalize_validator_data(raw_data)
