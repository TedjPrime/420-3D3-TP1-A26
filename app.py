import tkinter as tk

from modeles.portefeuille import Portefeuille
from observateurs.affichage_alertes import ObservateurAlertes
from observateurs.affichage_liste import ObservateurListe
from observateurs.affichage_portfolio import ObservateurPortfolio
from observateurs.affichage_prix import ObservateurPrix
from observateurs.journal_csv import ObservateurJournalCSV
from views.vue_alertes import VueAlertes
from views.vue_gestion import VueGestion
from views.vue_portfolio import VuePortfolio
from views.vue_prix import VuePrix


TITRES = {
    "AAPL": {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
    "GOOGL": {"quantite": 5, "seuil_haut": 160.0, "seuil_bas": 120.0},
    "MSFT": {"quantite": 8, "seuil_haut": 430.0, "seuil_bas": 380.0},
}
INTERVALLE_MS = 30000


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)
        self.fenetre.option_add("*Font", ("Segoe UI", 10))
        tk.Label(
            self.fenetre, text="Portfolio Tracker",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        self.portefeuille = Portefeuille(TITRES)
        self.vue_prix = VuePrix(self.fenetre)
        self.vue_portfolio = VuePortfolio(self.fenetre)
        self.vue_alertes = VueAlertes(self.fenetre)
        self.vue_gestion = VueGestion(
            self.fenetre,
            self.ajouter_titre,
            self.retirer_titre,
            self.modifier_titre,
        )

        for ticker in TITRES:
            self.vue_prix.ajouter_titre(ticker)

        self.portefeuille.ajouter_observateur(
            ObservateurPrix(self.vue_prix)
        )
        self.portefeuille.ajouter_observateur(
            ObservateurPortfolio(self.vue_portfolio)
        )
        self.portefeuille.ajouter_observateur(
            ObservateurAlertes(self.vue_alertes)
        )
        self.portefeuille.ajouter_observateur(
            ObservateurListe(self.vue_gestion)
        )
        self.portefeuille.ajouter_observateur(ObservateurJournalCSV())

        self.vue_gestion.afficher_titres(TITRES)
        self.rafraichir()
        self.fenetre.mainloop()

    def ajouter_titre(self, vue):
        ticker = vue.entry_ticker.get().strip().upper()
        quantite = vue.entry_quantite.get().strip()
        bas = vue.entry_seuil_bas_ajout.get().strip() or None
        haut = vue.entry_seuil_haut_ajout.get().strip() or None
        try:
            self.portefeuille.ajouter_titre(ticker, quantite, haut, bas)
            self.vue_prix.ajouter_titre(ticker)
            vue.vider(
                vue.entry_ticker,
                vue.entry_seuil_bas_ajout,
                vue.entry_seuil_haut_ajout,
            )
            vue.entry_quantite.insert(0, "1")
            vue.statut(
                f"{ticker} ajouté au portfolio ({quantite} action(s)).",
                "green",
            )
        except (ValueError, KeyError) as erreur:
            vue.statut(str(erreur), "red")

    def retirer_titre(self, vue):
        ticker = vue.ticker_selectionne()
        if ticker is None:
            vue.statut("Sélectionnez un titre à retirer.", "orange")
            return
        try:
            self.portefeuille.retirer_titre(ticker)
            self.vue_prix.retirer_titre(ticker)
            vue.statut(f"{ticker} retiré du portfolio.", "gray")
        except (ValueError, KeyError) as erreur:
            vue.statut(str(erreur), "red")

    def modifier_titre(self, vue):
        ticker = vue.ticker_selectionne()
        if ticker is None:
            vue.statut("Sélectionnez un titre à modifier.", "orange")
            return
        quantite = vue.entry_nouvelle_quantite.get().strip() or None
        bas = vue.entry_nouveau_seuil_bas.get().strip() or None
        haut = vue.entry_nouveau_seuil_haut.get().strip() or None
        try:
            self.portefeuille.modifier_titre(ticker, quantite, haut, bas)
            vue.vider(
                vue.entry_nouvelle_quantite,
                vue.entry_nouveau_seuil_bas,
                vue.entry_nouveau_seuil_haut,
            )
            vue.statut(f"{ticker} mis à jour.", "green")
        except (ValueError, KeyError) as erreur:
            vue.statut(str(erreur), "red")

    def rafraichir(self):
        self.portefeuille.rafraichir()
        self.fenetre.after(INTERVALLE_MS, self.rafraichir)
