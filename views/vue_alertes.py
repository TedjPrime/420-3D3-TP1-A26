import tkinter as tk


class VueAlertes:
    def __init__(self, parent):
        frame = tk.LabelFrame(
            parent, text="Alertes", padx=10, pady=10
        )
        frame.pack(fill=tk.X, padx=10, pady=5)
        self.label = tk.Label(
            frame, text="Aucune alerte", fg="gray",
            justify=tk.LEFT, wraplength=380
        )
        self.label.pack(anchor="w")
