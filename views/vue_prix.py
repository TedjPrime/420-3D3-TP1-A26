import tkinter as tk


class VuePrix:
    def __init__(self, parent):
        self.frame = tk.LabelFrame(
            parent, text="Prix en temps réel", padx=10, pady=10
        )
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        self._labels = {}
        self._frames = {}

    def ajouter_titre(self, ticker):
        if ticker in self._labels:
            return

        frame = tk.Frame(self.frame)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(
            frame, text=f"{ticker}:", width=8,
            font=("Segoe UI", 10, "bold"), anchor="w"
        ).pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)
        self._labels[ticker] = label
        self._frames[ticker] = frame

    def retirer_titre(self, ticker):
        self._labels.pop(ticker, None)
        frame = self._frames.pop(ticker, None)
        if frame is not None:
            frame.destroy()

    def afficher(self, lignes):
        for ticker, (texte, couleur) in lignes.items():
            if ticker in self._labels:
                self._labels[ticker].config(text=texte, fg=couleur)
