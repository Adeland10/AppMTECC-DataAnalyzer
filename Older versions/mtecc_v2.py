#coding: utf-8

import pandas as pd
import openpyxl as xl

#-------------------------------------------------------------------------------------------------
#importation du fichier excel et de la fenêtre contenant les raw data
filepath = r'C:\Users\adele\Bureau\INEM\Code\HNE PredictCFdec162k p1+3F508del and CastanierSoleneWT p1+3 and no cells in 5 6 20 06 24_comp.xlsx'
sheet= 'HNE PredictCFdec162k p1+3F508de'
df = pd.read_excel(filepath, sheet)
#print("fichier loaded") #vérif
# print(df.head())      #vérif

""" DATA TEST 
df_test=df.head()
"""
# groupby() de pandas pour regrouper par Marker
grouped = df.groupby('Marker')

#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue

def calculate_means(df):
    # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur
    means_dict = {}

    for marker, group in grouped:
        # Sélect 10 dernières lignes/valeurs pour chaque marqueur
        last_10_rows = group.tail(10)
        print(last_10_rows) # Verif 10 dernières valeurs de GT, Ieq, Iraw, PD, RT pour chaque marker
        
        # Calcul moyennes pour les colonnes GT, Ieq, Iraw, PD, RT  
        means_dict[marker] = {
            'GT': last_10_rows['GT'].mean(),
            'Ieq': last_10_rows['Ieq'].mean(),
            'Iraw': last_10_rows['Iraw'].mean(),
            'PD': last_10_rows['PD'].mean(),
            'RT': last_10_rows['RT'].mean()
        }

    return pd.DataFrame(means_dict).T  # .T --> transposition, plus facile à lire

#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de tous les puits
#def calculate_delta(means_df):
    deltas = {}
    markers = sorted(means_df.index)
    for i in range(1, len(markers)):
        marker1 = markers[i]
        marker0 = markers[i - 1]
        deltas[(marker0, marker1)] = means_df.loc[marker1] - means_df.loc[marker0]
    return deltas

def calculate_delta(means_df):
    deltas = {}
    delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
    markers = sorted(means_df.index)
    delta_index = 0
    
    for i in range(1, len(markers)):
        marker1 = markers[i]
        marker0 = markers[i - 1]
        delta_name = delta_names[delta_index] if delta_index < len(delta_names) else f"Δ{marker0}-{marker1}"
        deltas[delta_name] = means_df.loc[marker1] - means_df.loc[marker0]
        delta_index += 1
    
    return deltas
#-------------------------------------------------------------------------------------------------
# Appeler fonction pour calculer les moyennes des 10 dernières valeurs par marqueur
moyennes = calculate_means(df)
print("Moyennes des 10 dernières valeurs par marqueur :")
print(moyennes)

# Appeler fonction pour calculer les deltas
deltas = calculate_delta(moyennes)
"""print(deltas)"""
print("Deltas entre les marqueurs successifs :")
for delta_name, delta_values in deltas.items():
    print(f"{delta_name}:")
    print(delta_values)


#-------------------------------------------------------------------------------------------------
# Représentation des résultats --> Test 1 : HISTOGRAMME ???
