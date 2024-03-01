#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# récupération des mois de la base
mois_base = []
cursor.execute("SELECT date FROM Ventes GROUP BY date;")

for ligne in cursor.fetchall():
    mois_base.append(ligne[0][3:10]) #[3:10] prend la partie MM/AAAA dans JJ/MM/AAAA ; cela correspond au mois d'une année

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

      # vérification du mois (s'agit-il d'un mois qui existe dans la base ?)
      saisie = True
      while saisie:
        date = input("Entrez le mois recherché (MM/AAAA) : ")
        if date in mois_base:

            # Pour le mois demandé, donner à chaque manager la possibilité d'afficher :

            # degré d’alcool moyen est consommé dans l'établissement
            cursor.execute("SELECT AVG(C.degre) FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN '01/11/2022' AND '30/11/2022' AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?);", (nometab,))
            degre_moyen = cursor.fetchall()
            for degre, in degre_moyen:
                print (f"Degré d’alcool moyen consommé dans l'établissement : {round(degre,1)}. ")

            # quantité d’alcool vendue ce mois-ci :
            cursor.execute("SELECT SUM(C.quantite) FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN '01/11/2022' AND '30/11/2022' AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?);", (nometab,))
            quantite_mois = cursor.fetchall()
            for quantite, in quantite_mois:
                print (f"Quantité d’alcool vendue ce mois-ci : {round(quantite,2)}.")

        # Si la date n'existe pas dans la base, on demande si le manager veut re-saisir une nouvelle date
        else:
          next = input("Date introuvable ! Souhaitez-vous saisir une autre date (O/N) ? ")
          if next.upper() == "N": #"N" ou "n" arrêtent le programme
            saisie = False

# Si le matricule saisi n'est pas celui d'un manager, l'accès aux données est refusé
else: 
  print ("Accès refusé")

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()