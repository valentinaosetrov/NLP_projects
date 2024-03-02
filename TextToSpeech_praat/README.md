# Phonétique et synthèse de la parole 

- Projet du premier semestre M1 Traitement Automatique des Langues, 2022-23

Ce projet consiste en la concaténation de diphones enregistrés pour transformer un texte saisi en parole. 

65 logatomes ont été obtenus à partir de 15 mots suivants : 


la, les, dans, de, rues, quartier(s), Paris, fille(s), aime(nt), découvrir, parcourir, déambuler, parisienne(s), historique(s), pavé(e)(s), touristique(s)

Cela permet de créer des phrases comme : "la fille aime déambuler dans les quartiers touristiques de paris"

Le script praat :
- Création d’une boîte de dialogue/formulaire pour saisir la phrase à synthétiser
- Ouverture des fichiers principaux (dictionnaire, grid, wav)
- Traitement des mots et transcription
- Extraction des segments sonores à partir des intervalles pour créer la phrase sonore
- Modification de la prosodie
- Suppression des fichiers de transition pour améliorer l’organisation de la fenêtre Praat Object
- Écoute du résultat final (play)
