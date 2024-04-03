import string

def compter_occurrences(mots):
    # Initialisation du dictionnaire avec des compteurs pour chaque lettre
    occurrences = {lettre: 0 for lettre in string.ascii_lowercase}

    # Parcours de chaque mot dans la liste de mots
    for mot in mots:
        # Convertir le mot en minuscules
        mot = mot.lower()
        # Parcours de chaque lettre dans le mot
        for lettre in mot:
            occurrences[lettre] += 1

    # Tri du dictionnaire par valeur (nombre d'occurrences) dans l'ordre décroissant
    occurrences_triees = dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))
    
    return occurrences_triees

def main():
    # Chemin du fichier texte contenant les mots
    chemin_fichier = "french_5.txt"

    try:
        # Lecture du fichier texte
        with open(chemin_fichier, "r") as fichier:
            mots = fichier.read().splitlines()

        # Calcul des occurrences des lettres dans les mots
        occurrences_lettres = compter_occurrences(mots)

        # Affichage des occurrences des lettres dans l'ordre décroissant
        for lettre, occurrence in occurrences_lettres.items():
            print(f"{lettre}: {occurrence}")

    except FileNotFoundError:
        print("Le fichier spécifié est introuvable.")

if __name__ == "__main__":
    main()
