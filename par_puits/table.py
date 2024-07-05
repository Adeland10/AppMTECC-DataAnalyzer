#coding: utf-8

import pandas as pd

#-------------------------------------------------------------------------------------------------
#création tableau  excel avec valeurs de deltas 

def create_delta_table(deltas_par_puits):
    delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
    calculated_delta_names = ['ΔFsk + ΔVX770', 'ΔFsk + ΔVX770 + ΔApi']
    measures = ['GT', 'PD', 'Ieq', 'Iraw', 'RT']

    columns = pd.MultiIndex.from_product(
        [measures, delta_names + calculated_delta_names],
        names=['Measure', 'Delta']
    )
    wells = list(deltas_par_puits.keys())
    delta_table = pd.DataFrame(index=wells, columns=columns)

    for well, deltas in deltas_par_puits.items():
        for measure in measures:
            for delta_name in delta_names:
                value = deltas.get(delta_name, {}).get(measure, pd.NA)
                delta_table.loc[well, (measure, delta_name)] = value

            delta_fsk = deltas.get('ΔFsk/IBMX', {}).get(measure, pd.NA)
            delta_vx770 = deltas.get('ΔVX770', {}).get(measure, pd.NA)
            delta_api = deltas.get('ΔApi', {}).get(measure, pd.NA)
            
            delta_fsk_vx770 = delta_fsk + delta_vx770 if pd.notna(delta_fsk) and pd.notna(delta_vx770) else pd.NA
            delta_fsk_vx770_api = delta_fsk_vx770 + delta_api if pd.notna(delta_fsk_vx770) and pd.notna(delta_api) else pd.NA
            
            # Assign calculated deltas to delta_table
            delta_table.loc[well, (measure, 'ΔFsk + ΔVX770')] = delta_fsk_vx770
            delta_table.loc[well, (measure, 'ΔFsk + ΔVX770 + ΔApi')] = delta_fsk_vx770_api
                
    return delta_table