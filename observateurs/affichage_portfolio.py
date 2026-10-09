from observateurs.observateur import Observateur

class ObservateurPortfolio(Observateur):
    def __init__(self, vue):
        self.vue = vue

    def actualiser(self, sujet):
        d = sujet.get_donnees()
        if d["erreur"]:
            self.vue.label_maj.config(text=f"Erreur : {d['erreur']}", fg="red")
            return
        if not d["prix"]:
            return
        self.vue.label_valeur.config(text=f"Valeur totale : {d['valeur_totale']:.2f} $")
        v = d["variation"]
        self.vue.label_variation.config(
            text=f"{'▲' if v >= 0 else '▼'} {abs(v):.2f} $ depuis l'ouverture",
            fg="green" if v >= 0 else "red")
        if d["derniere_maj"]:
            self.vue.label_maj.config(text=f"Dernière mise à jour : {d['derniere_maj']}", fg="gray")
