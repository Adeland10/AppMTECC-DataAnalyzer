#coding: utf-8


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
# Fonction pour regrouper les puits par patient

def group_wells_by_patient(df):
    patient_wells = {1: ['A1', 'B1', 'A2', 'B2', 'C1', 'C2', 'D1', 'D2'],
                     2: ['A3', 'A4', 'B3', 'B4', 'C3', 'C4', 'D3', 'D4'],
                     3: ['A5', 'A6', 'B5', 'B6', 'C5', 'C6', 'D5', 'D6']}

    grouped_patients = {}
    for patient, wells in patient_wells.items():
        valid_wells = [well for well in wells if well in df['Well'].values]
        if valid_wells:
            grouped_patients[patient] = valid_wells

    return grouped_patients

#print(group_wells_by_patient(df)) #VERIFFFF