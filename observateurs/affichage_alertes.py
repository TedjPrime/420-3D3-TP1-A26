from observateurs.observateur import Observateur

class ObservateurAlertes(Observateur):
    def __init__(self, vue):
        self.vue = vue

    def actualiser(self, sujet):
        a = sujet.get_donnees()["alertes"]
        self.vue.label.config(text="\n".join(a) if a else "Aucune alerte", fg="red" if a else "gray")
