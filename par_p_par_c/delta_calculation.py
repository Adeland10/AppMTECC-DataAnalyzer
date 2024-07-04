import pandas as pd
import numpy as np


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit en les regroupant par patients 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']

def calculate_delta_by_well(df, means_dict):
    all_deltas = {}

    for well, markers in means_dict.items():
        deltas = {}
        markers_keys = sorted(markers.keys()) #trier marker en ordre croissant pour calculer deltas de manière séquentielle entre les marqueurs
    
        for i in range(1, len(markers_keys)):
            marker1 = markers_keys[i]
            marker0 = markers_keys[i - 1]
            delta_name = delta_names[i - 1]

        # Utiliser les moyennes globales pour calculer les deltas
            delta_GT = markers[marker1]['GT'] - markers[marker0]['GT']
            delta_Ieq = markers[marker1]['Ieq'] - markers[marker0]['Ieq']
            delta_Iraw = markers[marker1]['Iraw'] - markers[marker0]['Iraw']
            delta_PD = markers[marker1]['PD'] - markers[marker0]['PD']
            delta_RT = markers[marker1]['RT'] - markers[marker0]['RT']
            
            deltas[delta_name] = {
                'GT': round(delta_GT, 2),
                'Ieq': round(delta_Ieq, 2),
                'Iraw': round(delta_Iraw, 2),
                'PD': round(delta_PD, 2),
                'RT': round(delta_RT, 2)
            }

        all_deltas[well] = deltas #stocker les deltas calculés pour un puit
    
    return all_deltas


# Fonction pour calculer les deltas par patient et traitement

def calculate_deltas_means_by_treatment(df, patient_wells, means_dict):
    deltas_by_well = calculate_delta_by_well(df, means_dict)
    aggregated_conditions = {}

    for patient, info in patient_wells.items():
        wells = info['wells']
        type_patient = info['type']
        deltas_by_condition = {}

        for well, condition_chronique, condition_accute in wells:
            condition_key = (condition_chronique, condition_accute)
            if condition_key not in deltas_by_condition:
                deltas_by_condition[condition_key] = {delta: {measure: [] for measure in ['GT', 'Ieq', 'Iraw', 'PD', 'RT']} for delta in delta_names}

            for delta, measures in deltas_by_well[well].items():
                for measure, value in measures.items():
                    deltas_by_condition[condition_key][delta][measure].append(value)

        aggregated_conditions[patient] = {}
        for condition, deltas in deltas_by_condition.items():
            aggregated_conditions[patient][condition] = {delta: {measure: round(np.mean(values), 2) for measure, values in measures.items()} for delta, measures in deltas.items()}
    
    #print(f"Aggregated Conditions: {aggregated_conditions}")  # Debug print

    return aggregated_conditions

#-------------------------------------------------------------------------------------------------
# Fonction pour générer un tableau de valeurs des deltas 

def create_delta_table(aggregated_conditions):
    rows = []
    index = []

    for patient, conditions in aggregated_conditions.items():
        for (cond1, cond2), deltas in conditions.items():
            row = []
            for measure in ['GT', 'PD', 'Ieq', 'Iraw', 'RT']:
                for delta in delta_names:
                    if delta in deltas and measure in deltas[delta]:
                        row.append(deltas[delta][measure])
                    else:
                        row.append(np.nan)  # Ajouter une valeur NaN si le delta n'existe pas
            
            rows.append(row)
            index.append((patient, cond1, cond2))

    columns = pd.MultiIndex.from_product(
        [['GT', 'PD', 'Ieq', 'Iraw', 'RT'], delta_names],
        names=['Measure', 'Delta']
    )

    delta_table = pd.DataFrame(rows, index=pd.MultiIndex.from_tuples(index, names=['Patient', 'Condition1', 'Condition2']), columns=columns)
    return delta_table

