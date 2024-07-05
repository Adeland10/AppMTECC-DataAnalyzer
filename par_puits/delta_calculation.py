import pandas as pd


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']

def calculate_delta_by_well(df, means_df):
    all_deltas = {}
    wells = df['Well'].unique() #savoir combien de puits diff existent

    for well in wells:
        deltas = {}
        markers = sorted(means_df.index) #trier marker en ordre croissant pour calculer deltas de manière séquentielle entre les marqueurs
        delta_index = 0
    
        for i in range(1, len(markers)):
            marker1 = markers[i]
            marker0 = markers[i - 1]
            delta_name = delta_names[delta_index] if delta_index < len(delta_names) else f"Δ{marker0}-{marker1}"
            
        # Utiliser les moyennes globales pour calculer les deltas
            delta_GT = means_df.loc[marker1]['GT'] - means_df.loc[marker0]['GT']
            delta_Ieq = means_df.loc[marker1]['Ieq'] - means_df.loc[marker0]['Ieq']
            delta_Iraw = means_df.loc[marker1]['Iraw'] - means_df.loc[marker0]['Iraw']
            delta_PD = means_df.loc[marker1]['PD'] - means_df.loc[marker0]['PD']
            delta_RT = means_df.loc[marker1]['RT'] - means_df.loc[marker0]['RT']
            
            deltas[delta_name] = {
                'GT': round(delta_GT, 3),
                'Ieq': round(delta_Ieq, 3),
                'Iraw': round(delta_Iraw, 3),
                'PD': round(delta_PD, 3),
                'RT': round(delta_RT, 3)
            }
            delta_index += 1

        all_deltas[well] = deltas #stocker les deltas calculés pour un puit
    
    return all_deltas

