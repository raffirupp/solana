# utils/metrics.py

import numpy as np

def gini(array):
    """Berechnet den Gini-Koeffizienten für eine Liste von Werten (z. B. Stake)."""
    array = np.array(array, dtype=np.float64)  # explizit float64
    if np.amin(array) < 0:
        array -= np.amin(array)
    array += 1e-9  # für numerische Stabilität
    array = np.sort(array)
    n = array.size
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * array)) / (n * np.sum(array)) - (n + 1) / n


def top_n_share(values, n=10):
    """Berechnet den Anteil der Top-N Werte (z. B. Stake) am Gesamtwert."""
    array = np.sort(np.array(values))[::-1]
    top_sum = np.sum(array[:n])
    total = np.sum(array)
    return top_sum / total if total > 0 else 0
