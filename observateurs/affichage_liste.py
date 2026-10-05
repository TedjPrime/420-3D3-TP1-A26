from observateurs.observateur import Observateur

class ObservateurListe(Observateur):
    def __init__(self, vue_gestion):
        self.vue = vue_gestion

    def mettre_a_jour(self, sujet):
        self.vue.afficher_titres(sujet.get_donnees()["titres"])
