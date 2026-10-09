import yfinance as yf


def recuperer_prix(ticker):
    """Retourne (prix, ouverture) ou ValueError si le titre est introuvable."""
    info = yf.Ticker(ticker).fast_info
    prix = info["last_price"]
    if prix is None:
        raise ValueError(f"Le titre '{ticker}' n'existe pas.")
    return prix, info["open"]
