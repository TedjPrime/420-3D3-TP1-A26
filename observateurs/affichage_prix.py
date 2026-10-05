from observateurs.observateur import Observateur

def formater_prix(prix, ouverture):
    variation = (prix - ouverture) / ouverture * 100
    symbole = "▲" if variation >= 0 else "▼"
    couleur = "green" if variation >= 0 else "red"
    return f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", couleur


class ObservateurPrix(Observateur):
    def __init__(self, vue):
        self.vue = vue

    def mettre_a_jour(self, sujet):
        d = sujet.get_donnees()
        lignes = {t: formater_prix(*d["prix"][t]) if t in d["prix"] else ("Chargement...", "black")
                  for t in d["titres"]}
        self.vue.afficher(lignes)