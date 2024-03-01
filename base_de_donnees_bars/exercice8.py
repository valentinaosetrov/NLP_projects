#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# récupération des mois de la base
mois_base = []
cursor.execute("SELECT date FROM Ventes GROUP BY date;")
for ligne in cursor.fetchall():
    mois_base.append(ligne[0][3:10]) #[3:10] prend la partie MM/AAAA dans JJ/MM/AAAA ; cela correspond au mois de l'année

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

            # boissons les moins vendues dans l'établissement ce mois-ci :
            cursor.execute("SELECT C.type, C.nomboisson, COUNT(C.idBoisson) AS nb_ventes FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY C.nomboisson ORDER BY nb_ventes LIMIT 1;", (nometab,))
            moins_vendues = cursor.fetchall()
             # Affichage du résultat : 
            for type, boisson, ventes in moins_vendues:
                print (f"Boisson la moins vendue du mois ({ventes} vente(s)) : {boisson} ({type}). ")

            # employés ayant vendu le moins de boissons ce mois-ci :
            cursor.execute("SELECT V.matricule, COUNT(C.idBoisson) AS nb_ventes FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY V.matricule ORDER BY nb_ventes LIMIT 1;", (nometab,))
            moins_vendeurs = cursor.fetchall()
             # Affichage du résultat : 
            for matricule, ventes in moins_vendeurs:
                print (f"Moins bon vendeur du mois : employé {matricule} ({ventes} vente(s)).")


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