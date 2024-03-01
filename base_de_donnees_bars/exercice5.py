#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# récupération des matricules des managers
matricules_managers = []
cursor.execute("SELECT matricule FROM Employes WHERE profession='Manager';")
for ligne in cursor.fetchall():
    matricules_managers.append(ligne[0])

# vérification du matricule (s'agit-il d'un matricule manager ?)
identifiant = input("Entrez votre matricule : ")
if identifiant in matricules_managers:
  print("Voici les données de votre bar : ")
  
  # données accessibles par le matricule manager (à quels établissements donne-t-il accès ?)
  etablissements_manager = []
  cursor.execute("SELECT nometab FROM Etablissements WHERE matricule = ?;", (identifiant,))
  for ligne in cursor.fetchall():
    etablissements_manager.append(ligne[0])
    for nometab in etablissements_manager:
     # les données qui seront affichées sont les mêmes que dans l'exercice 3 (matricule employé, total de boissons vendues, montant de ce total vendu)
     cursor.execute("SELECT V.matricule, COUNT(V.idBoisson), SUM(prix) FROM Carte AS C, Ventes AS V WHERE C.idBoisson = V.idBoisson AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar =?) GROUP BY matricule;", (nometab,))
     donnees_manager = cursor.fetchall()
     
     #Affichage du résultat de la requête, si accès autorisé
     for employe, vente, montant in donnees_manager:
      print (f"Employé {employe} : {vente} boissons vendues, pour un total de {round(montant,2)} euros.") # montant arrondi

# Si le matricule saisi n'est pas celui d'un manager, l'accès aux données est refusé
else:
  print("Accès refusé")

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()