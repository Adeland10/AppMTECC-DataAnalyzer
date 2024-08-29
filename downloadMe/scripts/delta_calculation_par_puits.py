import pandas as pd


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']

def calculate_delta_by_well(df, means_dict):
    all_deltas = {}
    wells = df['Well'].unique() #savoir combien de puits diff existent

    for well in wells:
        deltas = {}
        
        if well not in means_dict:
            continue  # Skip wells with no data
        
        well_means = means_dict[well]

        # Extract basal values (assuming marker0 is the basal reference)
        marker0 = list(well_means.keys())[0]
        basal_values = well_means[marker0]
        deltas['Basal'] = {k: round(v, 3) for k, v in basal_values.items()}

        delta_index = 0
        markers = sorted(well_means.keys())

        for i in range(1, len(markers)):
            marker1 = markers[i]
            marker0 = markers[i - 1]
            delta_name = delta_names[delta_index] if delta_index < len(delta_names) else f"Δ{marker0}-{marker1}"

            delta_GT = well_means[marker1]['GT'] - well_means[marker0]['GT']
            delta_Ieq = well_means[marker1]['Ieq'] - well_means[marker0]['Ieq']
            delta_Iraw = well_means[marker1]['Iraw'] - well_means[marker0]['Iraw']
            delta_PD = well_means[marker1]['PD'] - well_means[marker0]['PD']
            delta_RT = well_means[marker1]['RT'] - well_means[marker0]['RT']

            deltas[delta_name] = {
                'GT': round(delta_GT, 2),
                'Ieq': round(delta_Ieq, 2),
                'Iraw': round(delta_Iraw, 2),
                'PD': round(delta_PD, 2),
                'RT': round(delta_RT, 2)
            }
            delta_index += 1

        all_deltas[well] = deltas #stocker les deltas calculés pour un puit
    
    return all_deltas
