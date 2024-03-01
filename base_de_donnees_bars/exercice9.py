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

            # boissons ayant rapporté le plus d'argent dans leur établissement ce mois-ci :
            cursor.execute("SELECT C.type, C.nomboisson, SUM(C.prix) AS caisse_boisson FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY C.nomboisson ORDER BY caisse_boisson DESC LIMIT 1;", (nometab,))
            meilleures_ventes = cursor.fetchall()
            # Affichage du résultat :
            for type, boisson, caisse in meilleures_ventes:
                print (f"Boisson ayant rapporté le plus d'argent au bar " + nometab + f" : {boisson} ({type}), {caisse} euros. ")

            # employés ayant rapporté le plus d'argent :
            cursor.execute("SELECT V.matricule, SUM(C.prix) AS caisse_employe FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date BETWEEN \"01/11/2022\" AND \"30/11/2022\" AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY V.matricule ORDER BY caisse_employe DESC LIMIT 1;", (nometab,))
            meilleurs_vendeurs = cursor.fetchall()
            # Affichage du résultat :
            for matricule, ventes in meilleurs_vendeurs:
                print (f"Employé ayant encaissé le plus d'argent dans le bar : {matricule}, {round(ventes,2)} euros.")


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