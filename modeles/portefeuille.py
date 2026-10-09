from datetime import datetime

from modeles.sujet import Sujet
from modeles.marche import recuperer_prix

class Portefeuille(Sujet):
     
    def __init__(self, titres):
        self._observateurs = []
        self._titres = titres          # ticker -> {quantite, seuil_haut, seuil_bas}
        self._prix = {}                # ticker -> (prix, ouverture)
        self._derniere_maj = None
        self._erreur = None
        self._origine = "init" 

    def ajouter_observateur(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def retirer_observateur(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def notifier(self):
        for observateur in self._observateurs:
            observateur.actualiser(self)

    def get_donnees(self):
        return {
            "titres": self._titres,
            "prix": self._prix,
            "derniere_maj": self._derniere_maj,
            "erreur": self._erreur,
            "origine": self._origine,
            "valeur_totale": self._calculer_valeur_totale(),
            "variation": self._calculer_variation(),
            "alertes": self._calculer_alertes()
        }
        
    def rafraichir(self):
        self._origine = "rafraichissement"
        self._erreur = None
        try:
            self._prix = {}
            for ticker in self._titres:
                prix, ouverture = recuperer_prix(ticker)
                self._prix[ticker] = (prix, ouverture)
            self._derniere_maj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            self._erreur = str(e)
        self.notifier()

    def ajouter_titre(self, ticker, quantite, seuil_haut=None, seuil_bas=None):
        ticker = ticker.strip().upper()

        if not ticker:
            raise ValueError("Le ticker est obligatoire.")

        if ticker in self._titres:
            raise ValueError(f"{ticker} est déjà dans le portefeuille.")

        quantite = int(quantite)

        if quantite <= 0:
            raise ValueError("La quantité doit être un entier positif.")

        if seuil_bas is not None:
            seuil_bas = float(seuil_bas)

            if seuil_bas <= 0:
                raise ValueError("Le seuil bas doit être positif.")

        if seuil_haut is not None:
            seuil_haut = float(seuil_haut)

            if seuil_haut <= 0:
                raise ValueError("Le seuil haut doit être positif.")

        if seuil_bas is not None and seuil_haut is not None:
            if seuil_bas >= seuil_haut:
                raise ValueError(
                    "Le seuil bas doit être inférieur au seuil haut."
                )

        try:
            prix, ouverture = recuperer_prix(ticker)
        except Exception as erreur:
            raise ValueError(
                f"Le titre '{ticker}' n'existe pas."
            ) from erreur

        if seuil_haut is None:
            seuil_haut = round(prix * 1.2, 2)

        if seuil_bas is None:
            seuil_bas = round(prix * 0.8, 2)

        self._titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": seuil_haut,
            "seuil_bas": seuil_bas,
        }

        self._origine = "ajout"
        self.notifier()


    def retirer_titre(self, ticker):
        ticker = ticker.upper()
        if ticker not in self._titres:
            raise KeyError(f"{ticker} absent du portefeuille")

        del self._titres[ticker]
        self._prix.pop(ticker, None)
        self._origine = "suppression"
        self.notifier()

    def modifier_titre(self, ticker, quantite=None, seuil_haut=None, seuil_bas=None):
        ticker = ticker.strip().upper()
        """Met à jour la quantité et/ou les seuils d'alerte du titre sélectionné.
        Chaque champ est optionnel : seuls ceux remplis sont modifiés, mais les
        deux seuils doivent être fournis ensemble pour rester cohérents."""

        if ticker not in self._titres:
            raise KeyError(f"{ticker} absent du portefeuille")

        if quantite is None and seuil_haut is None and seuil_bas is None:
            raise ValueError(
                "Entrez une nouvelle quantité et/ou de nouvelles alertes."
            )

        if quantite is not None:
            quantite = int(quantite)
            if quantite < 0:
                raise ValueError(
                    "La quantité doit être un nombre entier positif."
                )

        if seuil_haut is not None or seuil_bas is not None:
            if seuil_haut is None or seuil_bas is None:
                raise ValueError(
                    "Les deux alertes doivent être fournies ensemble."
                )

            seuil_bas = float(seuil_bas)
            seuil_haut = float(seuil_haut)

            if seuil_bas < 0 or seuil_haut < 0:
                raise ValueError(
                    "Les alertes doivent être des nombres positifs."
                )

            if seuil_bas >= seuil_haut:
                raise ValueError(
                    "L'alerte basse doit être inférieure à l'alerte haute."
                )

        if quantite is not None:
            self._titres[ticker]["quantite"] = quantite

        if seuil_bas is not None and seuil_haut is not None:
            self._titres[ticker]["seuil_bas"] = round(seuil_bas, 2)
            self._titres[ticker]["seuil_haut"] = round(seuil_haut, 2)

        self._origine = "modification"
        self.notifier()


    def _calculer_alertes(self):
        alertes = []
        for ticker, infos in self._titres.items():
            if ticker in self._prix:
                prix, _ = self._prix[ticker]
                if prix >= infos["seuil_haut"]:
                    alertes.append(f"⚠️ {ticker} dépasse le seuil haut ({prix:.2f} $)")
                elif prix <= infos["seuil_bas"]:
                    alertes.append(f"⚠️ {ticker} sous le seuil bas ({prix:.2f} $)")
        return alertes

    def _calculer_variation(self):
        valeur_ouverte = 0
        valeur_actuelle = 0

        for ticker, infos in self._titres.items():
            if ticker in self._prix:
                prix, ouverture = self._prix[ticker]
                valeur_actuelle += prix * infos["quantite"]
                valeur_ouverte += ouverture * infos["quantite"]

        return valeur_actuelle - valeur_ouverte

    def _calculer_valeur_totale(self):
        total = 0
        for ticker, infos in self._titres.items():
            if ticker in self._prix:
                prix, _ = self._prix[ticker]
                total += prix * infos["quantite"]
        return total