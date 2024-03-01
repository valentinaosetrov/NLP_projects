#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# récupération des dates de la base
dates_base = []
cursor.execute("SELECT date FROM Ventes GROUP BY date;")
for ligne in cursor.fetchall():
    dates_base.append(ligne[0])

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

      # vérification de la date (s'agit-il d'une date qui existe dans la base ?)
      saisie = True
      while saisie:
        date = input("Entrez la date recherchée (JJ/MM/AAAA) : ")
        if date in dates_base:

            # Pour la date demandée, donner à chaque manager la possibilité d'afficher :

            # employés ayant vendu le plus de cocktails du jour :
            cursor.execute("SELECT V.matricule, COUNT(C.idBoisson) AS nb_ventes, V.date FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND C.nomboisson = 'Cocktail du moment' AND date = ? AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY V.matricule ORDER BY nb_ventes DESC LIMIT 1;", (date,nometab,))
            max_cocktails = cursor.fetchall()
            # Affichage du résultat : (TOP 5)
            for matricule, ventes, date in max_cocktails:
                print (f"Employé ayant vendu le plus de cocktails du jour le {date} : {matricule}, {ventes} ventes. ")

            # employés ayant vendu le plus de bières pression :
            cursor.execute("SELECT V.matricule, COUNT(C.idBoisson) AS nb_ventes, V.date FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND C.nomboisson = 'Blonde pression' AND date = ? AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY V.matricule ORDER BY nb_ventes DESC LIMIT 1;", (date,nometab,))
            max_bieres = cursor.fetchall()
            # Affichage du résultat : (TOP 5)
            for matricule, ventes, date in max_bieres:
                print (f"Employé ayant vendu le plus de bières pression le {date} : {matricule}, {ventes} ventes. ")

        # Si la date n'existe pas dans la base, on demande si le manager veut re-saisir une nouvelle date
        else:
          next = input("Date introuvable ! Souhaitez-vous saisir une autre date (O/N) ? ")
        #"N" ou "n" arrêtent le programme
          if next.upper() == "N":
            saisie = False
       

# Si le matricule saisi n'est pas celui d'un manager, l'accès aux données est refusé
else: 
  print ("Accès refusé")

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()