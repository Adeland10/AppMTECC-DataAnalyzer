# Guide application MTECC Data Analyzer

## Introduction
Cette application de bureau MTECC Data Analyzer est conçue pour les chercheurs biologistes travaillant sur l'étude des mécanismes de transport ionique transmembrannaire dans le cadre de la recherche sur les traitements de la mucoviscidose. L'application permet de faciliter l'analyse des données obtenues via la Méthode des Techniques Électrophysiologiques de Courant Court-Circuit (MTECC), une méthode dérivée de la technique de la chambre d'Ussing utilisée pour mesurer le transport actif des ions à travers les tissus épithéliaux.

Avec MTEC Data Analyzer, les chercheurs peuvent :

1. Importer des Fichiers de Données du Robot MTECC : importation des données générées par la MTECC.

2. Effectuer des Calculs Automatisés : L'application propose des algorithmes d'analyse pour calculer directement les paramètres liés au transport ionique (delta sur les courbes de courant de court-circuit, flux ionique net) à partir des mesures brutes.

3. Visualiser et Interpréter les Données : Affichage des résultats dans des tableaux et des graphiques, facilitant l’interprétation des résultats par les chercheurs pour évaluer l'impact des médicaments ou d’autres substances sur le transport ionique (Na⁺, Cl⁻, etc.) témoignantde l'efficacité de la protéine CFTR mis en cause dans la maladie.

MTEC Data Analyzer est donc un outil indispensable pour les laboratoires de recherche biomédicale, facilitant la transition entre les données expérimentales et l'interprétation scientifique afin d'accélérer la découverte de traitements pour la mucoviscidose.

## Installation
1. Télécharger le dossier compressé `AppMTECC-DataAnalyzer.zip`.
2. Extrayez le dossier compressé `AppMTECC-DataAnalyzer.zip`.
3. Ouvrez le dossier extrait.

## Utilisation
1. Ouvrez le dossier `AppMTECC-DataAnalyzer` puis `Distribution` puis `dist`puis le dossier `MTECC Data Analyzer`.
2. Double-cliquez sur `MTECC Data Analyzer.exe` pour lancer l'application.
3. Importer le fichier issu de MTECC en format `.xlsx`.
4. Renseigner le dossier de sortie (là où les tableaux excel et graphiques générées par l'application seront sauvegardées).
5. Sélectionner les données que vous souhaitez générer (table of data, graph)
6. Appuyer sur le bouton `Generate` pour générer les données.
7. Attendre le message de confirmation et cliquez sur `OK`.
8. Vérifier la sauvegarde des données générées dans le dossier de sortie que vous avez renseigné.

NOTE : - Transformer le fichier `.dcd` de la MTECC en fichier `.csv` en utilisant l'application `MTECC24 DCD to csv2` en     suivant la légende du fichier `Légende - Plan de plaque MTECC.xlsx `.
       - Utiliser l'application Excel pour transformer le fichier `.csv` en fichier `.xlsx` 
       - voir fiche d'instruction MTECC Data Analyzer

## Structure des fichiers dans Distribution
- `dist/` contenant `MTECC Data Analyzer.exe` : Le fichier exécutable de l'application.
- `scripts/` : Contient les scripts Python nécessaires au fonctionnement de l'application.
- `assets/` : Contient les fichiers image et autres ressources utilisées par l'application.

## Support
Pour toute question ou assistance, veuillez contacter :
    - Adèle Faillé (adele.faille@live.fr) ou 
    - Iwona Pranke (iwona.pranke@inserm.fr).

 ## Creator
 @Adèle Faillé   
 for INEM in August 2024
