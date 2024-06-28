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
                'GT': delta_GT,
                'Ieq': delta_Ieq,
                'Iraw': delta_Iraw,
                'PD': delta_PD,
                'RT': delta_RT
            }
            delta_index += 1

        all_deltas[well] = deltas #stocker les deltas calculés pour un puit
    
    return all_deltas

#-------------------------------------------------------------------------------------------------
#création tableau  excel avec valeurs de deltas 

def create_delta_table(deltas_par_puits):
    delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
    columns = pd.MultiIndex.from_product(
        [['GT', 'PD', 'Ieq', 'Iraw', 'RT'], delta_names],
        names=['Measure', 'Delta']
    )
    wells = list(deltas_par_puits.keys())
    delta_table = pd.DataFrame(index=wells, columns=columns)

    for well, deltas in deltas_par_puits.items():
        for delta_name, delta_values in deltas.items():
            for measure, value in delta_values.items():
                delta_table.loc[well, (measure, delta_name)] = value

    return delta_table