### Création d'une boîte de dialogue/formulaire pour saisir la phrase à synthétiser ###

form Veillez insérer la phrase que vous souhaitez synthétiser
text phrase_synth
endform
pause Voici le contenu de la phrase synthétisée : 'phrase_synth$'

### Ouverture des fichiers principaux et enregistrement des variables ###

grille = Read from file: "valentina.TextGrid"
son = Read from file: "valentina.wav"
table_complete_dico = Read Table from tab-separated file: "dico1.txt"
# le son vide pour stocker les sons concaténés
son_final = Create Sound from formula: "sineWithNoise", 1, 0, 0.01, 44100, "0" 

### Préparation des variables pour les mots orthographiques/phonétiques à traiter ###

# initialiser une chaîne de caractère vide pour stocker la transcription phonétique
trans_phon$ = ""
# ajouter un espace au mot orthographique
phrase_synth$ = phrase_synth$ + " "
# calculer la longueur de la chaîne de caractères "phrase_synth"
longueur_phrase_synth= length (phrase_synth$)

### Traitement des mots et transcription ###

while longueur_phrase_synth > 0
	# trouver la position de l'espace dans la chaîne de caractère saisie
	espace_position = index (phrase_synth$, " ")
	# trouver le premier mot/début de la phrase
	mot1$ = left$ (phrase_synth$, espace_position - 1)
	# trouver le reste de la phrase
        phrase_synth$ = right$ (phrase_synth$, longueur_phrase_synth - espace_position)
	# m-à-j de la nouvelle longueur de la chaîne de caractère saisie
	longueur_phrase_synth = length (phrase_synth$)

	#transcription de l'orthographe vers phonétique à partir du dictionnaire
	select 'table_complete_dico'
	extraction = Extract rows where column (text): "orthographe", "is equal to", mot1$
	mot_phonetique$ = Get value: 1, "phonetique"
	trans_phon$ = trans_phon$ + mot_phonetique$
endwhile

#concatenation de la transcription phonétique
trans_phon$ = "_" + trans_phon$ + "_"

select 'grille'
nb_intervals = Get number of intervals: 1
longueur_mot = length (trans_phon$)

### Former les diphones à partir des caractères ###

for b from 1 to longueur_mot-1
		diphone$ = mid$ (trans_phon$, b, 2)
		char1_diphone$ = left$ (diphone$, 1)
		char2_diphone$ = right$ (diphone$, 1)
		printline 'diphone$'

### Extraire les segments sonores à partir des intervalles pour créer la phrase sonore ###

for a from 1 to nb_intervals - 1   
		select 'grille'
		st_interval = Get start time of interval: 1, a
		et_interval = Get end time of interval: 1, a
		lb_interval$ = Get label of interval: 1, a
		lb_interval_suiv$ = Get label of interval: 1, a+1
		et_interval_suiv = Get end time of interval: 1, a+1

		# vérifier si les caractères forment un diphone existant
		if (lb_interval$ = char1_diphone$ and lb_interval_suiv$ = char2_diphone$)
			# trouver les milieux des début et de la fin pour chaque diphone
			m1 = (et_interval - st_interval) /2 + st_interval
			m2 = (et_interval_suiv - et_interval) /2 + et_interval
			
			# trouver l'intersection avec zéro descendant
			select 'son'
			inter_zero_desc = To PointProcess (zeroes): 1, "no", "yes"
			select 'inter_zero_desc'

			idx1 = Get nearest index: 'm1'
			tmps_idx1 = Get time from index: 'idx1'
			idx2 = Get nearest index: 'm2'
			tmps_idx2 = Get time from index: 'idx2'

			# extraire le son à partir de nouveaux intervalles calculés
			select 'son'
			son_extrait = Extract part: tmps_idx1, tmps_idx2, "rectangular", 1, "no"
			# concatener 
			select 'son_final'
			plus 'son_extrait'
			son_final = Concatenate

		endif

endfor

endfor

### Modification de la prosodie ###

# Modifier la F0 

select 'son_final'
manip = To Manipulation: 0.01, 75, 600

pitch_f0 = Extract pitch tier

Remove points between: 0, 5.195760

Add point: 0.001, 210
Add point: 0.2, 220
Add point: 0.26, 210
Add point: 0.65, 220
Add point: 0.85, 210
Add point: 1.69, 205
Add point: 2.13, 215
Add point: 4.72, 220
Add point: 5, 200

select 'manip'
plus 'pitch_f0'
Replace pitch tier

select 'manip'
Get resynthesis (overlap-add)

# Modifier la durée

select 'manip'
duree = Extract duration tier

Add point: 0.001, 0.9
Add point: 0.70, 0.9
Add point: 0.701, 1
Add point: 1.30, 0.8
Add point: 1.50, 0.9
Add point: 1.70, 1.4
Add point: 1.80, 1.4
Add point: 1.99, 2.9
Add point: 2, 0.9
Add point: 2.96, 0.9
Add point: 2.961, 1
Add point: 3.25, 0.9
Add point: 3.30, 1.1
Add point: 3.45, 0.9
Add point: 4.20, 0.9
Add point: 4.201, 1.1
Add point: 4.50, 0.9
Add point: 4.97, 0.9
Add point: 5.01, 4
Add point: 5.07, 1

select 'manip'
plus 'duree'
Replace duration tier

select 'manip'
Get resynthesis (overlap-add)

### Renommage des fichiers importants ###

selectObject: "Sound chain"
Rename: "prosodie finale"

selectObject: "Sound chain"
Rename: "modifpitch"

selectObject: "Sound chain"
Rename: "sans modif prosodie"

### Suppression des fichiers de transition pour améliorer l'organisation de la fenêtre PraatObject ###

select all
minus TextGrid valentina
minus Sound valentina
minus Table dico1
minus Sound prosodie_finale
minus Sound sans_modif_prosodie
minus Manipulation chain
Remove

### Écouter le résultat final ###

pause Cliquer sur continue pour écouter le résultat final !
selectObject: "Sound prosodie_finale"
Play