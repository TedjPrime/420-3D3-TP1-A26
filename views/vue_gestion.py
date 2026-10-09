import tkinter as tk


class VueGestion:
    def __init__(self, parent, ajouter, retirer, modifier):
        self._retirer = retirer
        self._modifier = modifier

        frame = tk.LabelFrame(
            parent, text="Gérer les titres", padx=10, pady=10
        )
        frame.pack(fill=tk.X, padx=10, pady=5)

        ligne_ajout = tk.Frame(frame)
        ligne_ajout.pack(fill=tk.X)
        self.entry_ticker = self._champ(ligne_ajout, "Ticker", 8)
        self.entry_quantite = self._champ(
            ligne_ajout, "Qté", 5, "1"
        )
        self.entry_seuil_bas_ajout = self._champ(
            ligne_ajout, "Alerte basse", 7
        )
        self.entry_seuil_haut_ajout = self._champ(
            ligne_ajout, "Alerte haute", 7
        )
        tk.Button(
            ligne_ajout, text="Ajouter",
            command=lambda: ajouter(self)
        ).pack(side=tk.LEFT)

        tk.Label(
            frame,
            text="(Alertes optionnelles : calculées à ±20% du prix actuel)",
            font=("Segoe UI", 8), fg="gray"
        ).pack(anchor="w", pady=(2, 5))

        ligne_liste = tk.Frame(frame)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(
            ligne_liste, height=4, exportselection=False
        )
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(
            ligne_liste, text="Retirer",
            command=lambda: retirer(self)
        ).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        ligne_modif = tk.Frame(frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(
            ligne_modif, "Qté", 5
        )
        self.entry_nouveau_seuil_bas = self._champ(
            ligne_modif, "Alerte basse", 7
        )
        self.entry_nouveau_seuil_haut = self._champ(
            ligne_modif, "Alerte haute", 7
        )
        tk.Button(
            ligne_modif, text="Modifier sélection",
            command=lambda: modifier(self)
        ).pack(side=tk.LEFT)

        self.label_statut_titres = tk.Label(
            frame, text="", font=("Segoe UI", 9), fg="gray"
        )
        self.label_statut_titres.pack(anchor="w", pady=(5, 0))

    def _champ(self, parent, texte, width, valeur_defaut=""):
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    def afficher_titres(self, titres):
        selection = self.ticker_selectionne()
        self.listbox_titres.delete(0, tk.END)
        for ticker, infos in titres.items():
            self.listbox_titres.insert(
                tk.END,
                f"{ticker} — {infos['quantite']} action(s) "
                f"(alerte : {infos['seuil_bas']:.2f} $ / "
                f"{infos['seuil_haut']:.2f} $)"
            )
        if selection in titres:
            index = list(titres).index(selection)
            self.listbox_titres.selection_set(index)

    def ticker_selectionne(self):
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        return self.listbox_titres.get(selection[0]).split(" — ")[0]

    def statut(self, texte, couleur):
        self.label_statut_titres.config(text=texte, fg=couleur)

    @staticmethod
    def vider(*entries):
        for entry in entries:
            entry.delete(0, tk.END)
