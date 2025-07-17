# utils/preprocessing.py

def normalize_validator_data(raw_validators):
    """Transform raw Solana validator data into simplified structure."""
    normalized = []
    for v in raw_validators:
        # Versuche delta-Wert aus der letzten epochCredits-Zeile zu extrahieren
        credits = 0
        epoch_credits = v.get("epochCredits", [])
        if isinstance(epoch_credits, list) and len(epoch_credits) > 0:
            last_entry = epoch_credits[-1]
            if isinstance(last_entry, list) and len(last_entry) == 3:
                credits = last_entry[2]  # delta-Wert

        normalized.append({
            "validator_name": v.get("nodePubkey", "Unknown"),
            "stake": int(v.get("activatedStake") or 0) / 1_000_000_000,  # in SOL
            "commission": v.get("commission", 0),
            "last_vote": v.get("lastVote", 0),
            "credits": credits
        })
    return normalized
