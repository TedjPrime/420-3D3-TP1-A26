from observateurs.observateur import Observateur


class ObservateurJournalCSV(Observateur):

    def __init__(self, fichier="portfolio.csv"):
        self.fichier = fichier

    def mettre_a_jour(self, sujet):
        d = sujet.get_donnees()
        if d["origine"] != "rafraichissement" or d["erreur"]:
            return
        with open(self.fichier, "a") as f:
            for t, (prix, ouv) in d["prix"].items():
                f.write(f"{d['derniere_maj']},{t},{prix:.2f},{ouv:.2f}\n")