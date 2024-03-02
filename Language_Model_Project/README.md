# Estimating a Language Model to Generate Wine Reviews

- Enseignant : Armand Stricker
- Projet de M1 TAL INALCO, 2022-23

Ce projet consiste en la création d'un programme capable d'écrire automatiquement des critiques de vin, similaires à celles trouvées sur le site web de Wine Spectator, en utilisant un modèle de langage.

Le script (review_generator.py) génère des critiques de vin en se basant sur un ensemble de données d'entraînement (wine_test.txt). Il utilise une approche naïve de Bayes pour créer une table de probabilités conditionnelles à partir des trigrammes (avec nltk) de mots extraits des critiques existantes. Ensuite, il génère de nouvelles critiques en sélectionnant de manière probabiliste les mots suivants en fonction des deux mots précédents.
