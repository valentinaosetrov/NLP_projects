import gensim
import random

# Modèles disponibles à https://fauconnier.github.io/#data
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin", binary=True, unicode_errors="ignore")

# Définir le mot à trouver
keys = list(model.key_to_index.keys()) # liste tous les termes présents dans le modèle
#random.seed(42) # Seed pour développer le jeu et ne pas sélectionner un nouveau mot à chaque exécution du code.tester de nouveaux mots
notre_mot = random.choice(keys) # sélectionner un nouveau mot à chaque exécution
#print(notre_mot)
#model.most_similar("tendue")

# Initialisation du compteur de tentatives
tentatives = 0

while True:
    entree = input("Entrez un mot : ")
    
    # Vérifier si le mot entré est dans le vocabulaire du modèle
    if entree not in model:
        print("Le mot n'est pas dans le vocabulaire.")
        continue
    
    # Comparer le mot entré avec le mot à deviner en utilisant la similarité cosinus
    similarity_score = model.similarity(entree, notre_mot)
    
    # Si le mot entré est idnetique au mot à deviner, le joueur a gagné et le jeu est terminé
    if entree == notre_mot:
        tentatives += 1 # incrémenter cette dernière tentative
        print("Bravo ! Vous avez deviné le mot en", tentatives, "tentatives ! \U0001F973 \U0001F973 \U0001F973 ")
        break
    # Afficher si le mot entré est proche ou non du mot à deviner.
    elif similarity_score >=0.8:
        print(f"Vous êtes très proche ! \U0001F929 {similarity_score:.2f}")   
    elif similarity_score >= 0.6:
        print(f"Vous vous rapprochez ! \U0001F609 {similarity_score:.2f}")
    elif similarity_score >= 0.4:
        print(f"Vous êtes sur la bonne voie, continuez ! \U0001F642 {similarity_score:.2f}")
    else:
        print(f"Vous êtes encore loin du mot à deviner. \U0001F615 {similarity_score:.2f}")    
    tentatives += 1 # incrémenter le compteur de tentatives à chaque essai
