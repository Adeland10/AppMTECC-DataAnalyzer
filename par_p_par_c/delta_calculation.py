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

    return aggregated_conditions


#-------------------------------------------------------------------------------------------------
# Fonction pour générer un tableau de valeurs des deltas 
def create_delta_tables(aggregated_conditions):
    rows_base = []
    rows_calculated = []
    index = []
    delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
    calculated_delta_names = ['ΔFsk + ΔVX770', 'ΔFsk + ΔVX770 + ΔApi']
    measures = ['GT', 'PD', 'Ieq', 'Iraw', 'RT']
    
    for patient, conditions in aggregated_conditions.items():
        for (cond1, cond2), deltas in conditions.items():
            row_base = []
            row_calculated = []
            for measure in measures:
                # Fill in the base delta values
                for delta in delta_names:
                    if delta in deltas and measure in deltas[delta]:
                        row_base.append(deltas[delta][measure])
                    else:
                        row_base.append(np.nan)  # Add NaN if the delta does not exist

                # Calculate the new deltas
                delta_fsk = deltas.get('ΔFsk/IBMX', {}).get(measure, np.nan)
                delta_vx770 = deltas.get('ΔVX770', {}).get(measure, np.nan)
                delta_api = deltas.get('ΔApi', {}).get(measure, np.nan)
                
                delta_fsk_vx770 = np.nan if np.isnan(delta_fsk) or np.isnan(delta_vx770) else delta_fsk + delta_vx770
                delta_fsk_vx770_api = np.nan if np.isnan(delta_fsk_vx770) or np.isnan(delta_api) else delta_fsk_vx770 + delta_api
                
                row_calculated.append(delta_fsk_vx770)
                row_calculated.append(delta_fsk_vx770_api)
            
            rows_base.append(row_base)
            rows_calculated.append(row_calculated)
            index.append((patient, cond1, cond2))
    
    columns_base = pd.MultiIndex.from_product([measures, delta_names], names=['Measure', 'Delta'])
    columns_calculated = pd.MultiIndex.from_product([measures, calculated_delta_names], names=['Measure', 'Delta'])
    
    delta_table_base = pd.DataFrame(rows_base, index=pd.MultiIndex.from_tuples(index, names=['Patient', 'Condition1', 'Condition2']), columns=columns_base)
    delta_table_calculated = pd.DataFrame(rows_calculated, index=pd.MultiIndex.from_tuples(index, names=['Patient', 'Condition1', 'Condition2']), columns=columns_calculated)
    
    return delta_table_base, delta_table_calculated

