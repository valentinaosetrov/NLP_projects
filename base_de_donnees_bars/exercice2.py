#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# Statistiques globales à l'échelle du groupe :

# nombre total de bars :
cursor.execute("SELECT COUNT(idEtablissements) AS nbEtablissements FROM Etablissements; ")
nb_bars = cursor.fetchall()

# nombre total d'employés :
cursor.execute("SELECT COUNT(matricule) AS nbEmployes FROM Employes;")
nb_employes = cursor.fetchall()

# managers de bars : 
cursor.execute("SELECT prenom, nom, nometab FROM Employes AS EMP, Etablissements AS ETA WHERE (EMP.matricule = ETA.matricule) GROUP BY nom;") # la jointure sur la clé matricule permet de ne retenir que les managers
stats_managers = cursor.fetchall()

# nombre d’employés pour chaque profession :
cursor.execute("SELECT COUNT(matricule), profession FROM Employes GROUP BY profession;")
stats_professions = cursor.fetchall()

# revenu total du groupe :
cursor.execute("SELECT SUM(prix) AS revenu FROM Ventes JOIN Carte ON Ventes.idBoisson = Carte.idBoisson")
revenu = cursor.fetchall()

# Affichage des résultats des 5 requêtes, dans l'ordre des requêtes : 
print("Les statistiques globales à l'échelle du groupe :")
print("\t")
for nb in nb_bars:
    print(f"Le nombre total des bars est {nb[0]}.")
for nbemp in nb_employes:
    print(f"Le nombre total d'employés est {nbemp[0]}.")
print("\t")
for prenom, nom, nombar in stats_managers:
    print(f"{prenom} {nom} dirige le bar {nombar}.")
print("\t")
for nbp, prof in stats_professions:
    print(f"Il y a {nbp} {prof}s.")
print("\t")
for rev in revenu:
    print(f"Le revenu total est de {round(rev[0],2)} euros.") #le revenu est arrondi


# on enregistre toutes les modifications :
bdd.commit()

bdd.close()