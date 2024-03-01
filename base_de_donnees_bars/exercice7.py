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

          # nombre de ventes effectuées ce jour-là par les employés d'un manager donné :
          cursor.execute("SELECT E.nombar, COUNT(V.idBoisson) FROM Employes AS E, Ventes AS V WHERE (E.matricule = V.matricule) AND V.date = ? AND V.matricule IN (SELECT matricule FROM Employes WHERE nombar = ?);", (date,nometab,))
          ventes_jour = cursor.fetchall()
          # Affichage du résultat : 
          for bar, vente in ventes_jour:
            print(f"Les employés de votre établissement ({bar}) ont vendu {vente} boissons le " + date)
    
          # montant total de ces ventes :
          cursor.execute("SELECT SUM(prix) FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date = ? AND V.matricule in (SELECT matricule from Employes WHERE nombar = ?);", (date,nometab,))
          totaux_jour = cursor.fetchall()
          # Affichage du résultat :
          for montant in totaux_jour:
           print (f"Total des ventes le " + date + f" : {round(montant[0],2)} euros.")
    
          # bénéfice par employé du bar :
          cursor.execute("SELECT V.matricule, SUM(prix) FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) AND V.date = ? AND V.matricule in (SELECT matricule from Employes WHERE nombar = ?) GROUP BY V.matricule;", (date,nometab,))
          employe_jour = cursor.fetchall()
          # Affichage du résultat : 
          for employe, benefice in employe_jour:
           print (f"Bénéfice de l'employé {employe} : {round(benefice,2)} euros le " + date)

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