#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import csv


bdd = sqlite3.connect('bars.db')
cursor = bdd.cursor()

# Création des 4 tables, indication des clés primaires, clés étrangères et d'autres attributs présents dans les fichiers donnés

cursor.execute("CREATE TABLE Employes (matricule TEXT PRIMARY KEY, prenom TEXT NOT NULL, nom TEXT NOT NULL, profession TEXT NOT NULL, nombar TEXT NOT NULL);")
cursor.execute("CREATE TABLE Etablissements (idEtablissements INTEGER PRIMARY KEY AUTOINCREMENT, nometab TEXT NOT NULL, adresse TEXT NOT NULL, numtel INTEGER NOT NULL, matricule TEXT NOT NULL, FOREIGN KEY (matricule) REFERENCES Employes(matricule));")
cursor.execute("CREATE TABLE Carte (idBoisson INTEGER PRIMARY KEY, nomboisson TEXT NOT NULL, type TEXT NOT NULL, prix REAL NOT NULL, degre REAL, quantite REAL NOT NULL);")
cursor.execute("CREATE TABLE Ventes (idVentes INTEGER PRIMARY KEY AUTOINCREMENT, matricule TEXT NOT NULL, idBoisson INTEGER NOT NULL, date TEXT NOT NULL, FOREIGN KEY (matricule) REFERENCES Employes(matricule), FOREIGN KEY (idBoisson) REFERENCES Carte(idBoisson));")
bdd.commit()

# ouverture et insertion dans les fichiers :
# pour chaque fichier : ouverture du fichier csv, insertion des attributs correspondants aux valeurs déjà existantes dans les fichiers.

PATH = "/home/valentina/Desktop/TAL/BDD/projet/" #il faut changer le chemin absolu afin que l'ouverture des fichiers se fasse dans le bon endroit pour celle/celui qui exécute la base de données

fichierEmployes = open(PATH+'employes.csv', 'rt')
CSVEmployes = csv.DictReader(fichierEmployes, delimiter="\t")
for ligne in CSVEmployes:
    cursor.execute("INSERT INTO Employes(matricule, prenom, nom, profession, nombar) VALUES (:Matricule, :Prenom, :Nom, :Profession, :Nom_Bar)", ligne)
fichierEmployes.close()

fichierEtablissements = open(PATH+'etablissements.csv', 'rt')
CSVEtablissements = csv.DictReader(fichierEtablissements, delimiter="\t")
for ligne in CSVEtablissements:
    cursor.execute("INSERT INTO Etablissements(nometab, adresse, numtel, matricule) VALUES (:Name, :Adresse, :NumTel, :Manager_Id)", ligne)
fichierEmployes.close()

fichierCarte = open(PATH+'carte.csv', 'rt')
CSVCarte = csv.DictReader(fichierCarte, delimiter="\t")
for ligne in CSVCarte:
    cursor.execute("INSERT INTO Carte(idBoisson, nomboisson, type, prix, degre, quantite) VALUES (:Id_Boisson, :Nom, :Type, :Prix, :Degre, :Quantite)", ligne)
fichierEmployes.close()

fichierVentes = open(PATH+'ventes.csv', 'rt')
CSVVentes = csv.DictReader(fichierVentes, delimiter="\t")
for ligne in CSVVentes:
    cursor.execute("INSERT INTO Ventes(matricule, idBoisson, date) VALUES (:Employe_Id, :Boisson_Id, :Date)", ligne)
fichierEmployes.close()

# on enregistre toutes les modifications :
bdd.commit()

bdd.close()