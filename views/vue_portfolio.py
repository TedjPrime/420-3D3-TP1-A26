import tkinter as tk


class VuePortfolio:
    def __init__(self, parent):
        frame = tk.LabelFrame(
            parent, text="Mon portfolio", padx=10, pady=10
        )
        frame.pack(fill=tk.X, padx=10, pady=5)
        self.label_valeur = tk.Label(
            frame,
            text="Valeur totale : calcul en cours...",
            font=("Segoe UI", 13, "bold"),
        )
        self.label_valeur.pack()
        self.label_variation = tk.Label(frame, text="")
        self.label_variation.pack()
        self.label_maj = tk.Label(
            parent, text="", font=("Segoe UI", 9), fg="gray"
        )
        self.label_maj.pack(pady=5)
