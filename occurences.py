import argparse
import string
import yaml

def compter_occurrences(mots):
    # Initialisation du dictionnaire avec des compteurs pour chaque lettre
    occurrences = {lettre: 0 for lettre in string.ascii_lowercase}

    # Parcours de chaque mot dans la liste de mots
    for mot in mots:
        # Convertir le mot en minuscules
        mot = mot.lower()
        # Parcours de chaque lettre dans le mot
        for lettre in mot:
            # Incrémentation du compteur de la lettre
            occurrences[lettre] += 1

    # Tri du dictionnaire par valeur (nombre d'occurrences) dans l'ordre décroissant
    occurrences_triees = dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))
    
    return occurrences_triees

def ecrire_resultat(resultat, chemin_sortie):
    # Écriture du résultat dans un fichier YAML
    with open(chemin_sortie, "w") as fichier_sortie:
        yaml.dump(resultat, fichier_sortie)

def main():
    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Compte les occurrences de chaque lettre dans un fichier texte et écrit le résultat dans un fichier YAML.")
    parser.add_argument("fichier_entree", help="Chemin vers le fichier texte d'entrée contenant les mots.")
    parser.add_argument("-o", "--fichier_sortie", help="Chemin vers le fichier de sortie où écrire le résultat en format YAML. Par défaut, 'occurences.yaml'.")

    # Parsing des arguments de la ligne de commande
    args = parser.parse_args()

    # Chemin du fichier texte d'entrée
    chemin_entree = args.fichier_entree
    # Chemin du fichier de sortie
    chemin_sortie = args.fichier_sortie if args.fichier_sortie else "occurences.yaml"

    try:
        # Lecture du fichier texte
        with open(chemin_entree, "r") as fichier:
            mots = fichier.read().splitlines()

        # Calcul des occurrences des lettres dans les mots
        occurrences_lettres = compter_occurrences(mots)

        # Écriture du résultat dans un fichier YAML de sortie
        ecrire_resultat(occurrences_lettres, chemin_sortie)

        print("Le résultat a été écrit dans le fichier YAML de sortie.")

    except FileNotFoundError:
        print("Le fichier spécifié est introuvable.")

if __name__ == "__main__":
    main()
