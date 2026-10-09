def entier_positif(texte):
    valeur = int(texte)
    if valeur < 0:
        raise ValueError
    return valeur

def flottant_positif(texte):
    valeur = float(texte)
    if valeur < 0:
        raise ValueError
    return valeur