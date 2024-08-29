import pandas as pd
import openpyxl as xl
import numpy as np


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue

def calculate_means_by_well(df):
    means_dict = {}     # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur
    grouped = df.groupby(['Well', 'Marker'])        # groupby() de pandas pour regrouper par Marker


    for (well, marker), group in grouped:
        last_10_rows = group.tail(10)             # Sélect 10 dernières lignes/valeurs pour chaque marqueur

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



#return pd.DataFrame(means_dict).T  # .T --> transposition, plus facile à lire
