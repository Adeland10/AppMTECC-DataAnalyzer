#coding: utf-8

import pandas as pd



#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue pour les colonnes GT, Ieq, Iraw, PD, RT  

def calculate_means(df):
    means_dict = {}     # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur
    grouped = df.groupby(['Well', 'Marker']) # groupby() de pandas pour regrouper par Marker

    for (well, marker), group in grouped:
        last_10_rows = group.tail(10)         # Sélect 10 dernières lignes/valeurs pour chaque marqueur
        #print(last_10_rows) # Verif 10 dernières valeurs de GT, Ieq, Iraw, PD, RT pour chaque marker
        
        if well not in means_dict:
            means_dict[well] = {}

        means_dict[well][marker] = {
            'GT': last_10_rows['GT'].mean(),
            'Ieq': last_10_rows['Ieq'].mean(),
            'Iraw': last_10_rows['Iraw'].mean(),
            'PD': last_10_rows['PD'].mean(),
            'RT': last_10_rows['RT'].mean()
        }

    return means_dict 

#-------------------------------------------------------------------------------------------------
# Fonction pour analyser la colonne description 

def parse_description(description):
    parts = description.split('_')
    type_patient = parts[0]
    patient_name = parts[1]
    condition_chronique = parts[2] if len(parts) > 2 else None
    condition_accute = parts[3] if len(parts) > 3 else None
    return type_patient, patient_name, condition_chronique, condition_accute

#-------------------------------------------------------------------------------------------------
# Fonction pour regrouper les puits par patient
def group_wells_by_patient(df):
    patient_wells = {}
    for well, desc in zip(df['Well'], df['Description']):
        type_patient, patient_name, condition_chronique, condition_accute = parse_description(desc)
        if patient_name not in patient_wells:
            patient_wells[patient_name] = {'type': type_patient, 'wells': []}
        patient_wells[patient_name]['wells'].append((well, condition_chronique, condition_accute))
    return patient_wells


