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

# données accessibles par le matricule manager (à quels établissements donne-t-il accès ?)
  etablissements_manager = []
  cursor.execute("SELECT nometab FROM Etablissements WHERE matricule = ?;", (identifiant,));
  for ligne in cursor.fetchall():
    etablissements_manager.append(ligne[0])
    for nometab in etablissements_manager:



      # nombre de boissons à supprimer :
      nb_suppr = int(input("Combien de boissons les moins rentables supprimer ? "))

      # vérification que ce nombre est inférieur au nombre total de boissons à la carte (44) :
      if nb_suppr <= 44:
       print (f"Les {nb_suppr} boissons les moins rentables sont à présent supprimées de la carte.")
       while nb_suppr > 0:
        # identification de la boisson rapportant le moins d'argent dans l'établissement
        cursor.execute("SELECT C.idBoisson, C.nomboisson, C.type, C.prix, C.degre, C.quantite FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY C.nomboisson ORDER BY SUM(C.prix) LIMIT 1;", (nometab,))
        moins_rentables = cursor.fetchall()
        for moins_rentable in moins_rentables:
                idBoisson, nomboisson, type, prix, degre, quantite = moins_rentable
                cursor.execute("DELETE FROM Carte WHERE idBoisson = ?;", (idBoisson,))
                nb_suppr -= 1
      # message d'erreur si le nombre excède celui des boissons à la carte
      else:
         print("Le nombre saisi excède celui des boissons à la carte !")
      
      # nombre de boissons à supprimer :
      nb_supprim = int(input("Combien de boissons les moins consommées supprimer ? "))
      # vérification que ce nombre est inférieur au nombre total de boissons à la carte (44) :
      if nb_supprim <= 44:
       print (f"Les {nb_supprim} boissons les moins consommées sont à présent supprimées de la carte.")
       while nb_supprim > 0:
        # identification de la boisson la moins consommée dans l'établissement
        cursor.execute("SELECT C.idBoisson, C.nomboisson, C.type, C.prix, C.degre, C.quantite FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY C.nomboisson ORDER BY COUNT(C.idBoisson) LIMIT 1;", (nometab,))
        moins_vendues = cursor.fetchall()
        for moins_vendue in moins_vendues:
                idBoisson, nomboisson, type, prix, degre, quantite = moins_vendue
                cursor.execute("DELETE FROM Carte WHERE idBoisson = ?;", (idBoisson,))
                nb_supprim -= 1
      # message d'erreur si le nombre excède celui des boissons à la carte
      else:
         print("Le nombre saisi excède celui des boissons à la carte !")

# Si le matricule saisi n'est pas celui d'un manager, l'accès aux données est refusé
else: 
  print ("Accès refusé")

bdd.commit()
bdd.close()