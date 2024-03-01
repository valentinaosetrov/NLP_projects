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

            # Donner à chaque manager la possibilité d'afficher :

            # nombre de ventes effectuées ce mois-ci par les employés d'un manager donné : (affiche le nom du bar du manager inscrit et le nombre total des ventes effectué par ses employés)
            cursor.execute("SELECT E.nombar, COUNT(V.idBoisson) FROM Employes AS E, Ventes AS V WHERE (E.matricule = V.matricule) AND V.date BETWEEN '01/11/2022' AND '30/11/2022' AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY E.nombar;", (nometab,))
            ventes_mensuelles = cursor.fetchall()
            # Affichage du résultat : 
            for bar, vtotal in ventes_mensuelles:
              print (f"Les employés de votre établissement ({bar}) ont vendu {vtotal} boissons ce mois-ci. ")

            # montant total de ces ventes : (affiche le nom du bar du manager inscrit et le montant total des ventes effectuées ce mois-ci)
            cursor.execute("SELECT E.nombar, SUM(prix) FROM Employes AS E, Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND (E.matricule = V.matricule) AND V.date BETWEEN '01/11/2022' AND '30/11/2022' AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) ORDER BY E.nombar;", (nometab,))
            montant_mensuel = cursor.fetchall()
            # Affichage du résultat : 
            for nbar, mtotal in montant_mensuel:
                print (f"Total des ventes mensuelles de {nbar} : {round(mtotal,2)} euros.") # montant arrondi

            # bénéfice par employé du bar : (affiche le matricule de l'employé et son benéfice pour les ventes effectuées ce mois-ci)
            cursor.execute("SELECT V.matricule, SUM(prix) FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND date BETWEEN '01/11/2022' AND '30/11/2022' AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?) GROUP BY matricule;", (nometab,))
            benefice_employe = cursor.fetchall()
            # Affichage des résultats : 
            for employe, benef in benefice_employe:
             print (f"Bénéfice de l'employé {employe} : {round(benef,2)} euros ce mois-ci.") # montant arrondi

        # Si la date n'existe pas dans la base, on demande si le manager veut re-saisir une nouvelle date
        else:
          next = input("Date introuvable ! Souhaitez-vous saisir une autre date (O/N) ? ")
          if next.upper() == "N": #"N" ou "n" arrêtent le programme
            saisie = False

# Si le matricule saisi n'est pas celui d'un manager, l'accès aux données est refusé
else:
  print("Accès refusé")

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()