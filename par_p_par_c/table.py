#coding: utf-8

import pandas as pd
import numpy as np


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

