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
        pass

    def retirer_observateur(self, observateur):
        pass

    def notifier(self):
        pass

    def get_donnees(self):
        pass

    def rafraichir(self):
        pass

    def ajouter_titre(self, ticker, quantite, seuil_haut=None, seuil_bas=None):
        pass

    def retirer_titre(self, ticker):
        pass

    def modifier_titre(self, ticker, quantite=None, seuil_haut=None, seuil_bas=None):
        pass