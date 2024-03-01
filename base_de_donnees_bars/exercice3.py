#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# nombre total de boissons vendues pour chaque employé :
# ceci est la première partie de la requête qui sera amélioré par la suite (et ne sera pas affichée).
cursor.execute("SELECT matricule, COUNT(idBoisson) FROM Ventes GROUP BY matricule;")
ventes_par_employe = cursor.fetchall()

# requête finale dont le résultat sera affiché :
# nombre total de boissons vendues pour chaque employé et le montant total associé à ces ventes (par employé) : 
cursor.execute("SELECT matricule, COUNT(V.idBoisson), SUM(prix) FROM Carte AS C, Ventes AS V WHERE C.idBoisson = V.idBoisson GROUP BY matricule;")
revenu_par_employe = cursor.fetchall()

# Affichage des résultats de la deuxième requête : 
for employe, vente, montant in revenu_par_employe:
    print(f"Employé {employe} : {vente} boissons vendues, pour un total de {round(montant,2)} euros.") # le montant est arrondi

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()