#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# date à laquelle le moins de ventes ont été enregistrées et le nombre de ces ventes :
cursor.execute("SELECT date, COUNT(idVentes) AS nb_ventes FROM Ventes GROUP BY date ORDER BY nb_ventes LIMIT 1;") #LIMIT 1 car il nous faut une seule date
date_ventes_min = cursor.fetchall()
# Affichage du résultat :
for date, nb_ventes in date_ventes_min:
    print(f"Le {date} est la date à laquelle un minimum de {nb_ventes} ventes ont été enregistrées.")

# date à laquelle les bénéfices ont été les moins importants et le montant des bénéfices :
cursor.execute("SELECT date, SUM(prix) as montant_ventes FROM Carte AS C, Ventes AS V WHERE (C.idBoisson = V.idBoisson) GROUP BY date ORDER BY montant_ventes LIMIT 1;") #LIMIT 1 car il nous faut une seule date
date_revenu_min = cursor.fetchall()
# Affichage du résultat
for date, montant_ventes in date_revenu_min:
    print(f"Le {date} est la date à laquelle un bénéfice minimum de {round(montant_ventes,2)} euros a été encaissé.")

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()