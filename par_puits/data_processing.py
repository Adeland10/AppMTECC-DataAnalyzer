import pandas as pd
import openpyxl as xl
import numpy as np


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue

def calculate_means(df):
    # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur
    means_dict = {}
    # groupby() de pandas pour regrouper par Marker
    grouped = df.groupby('Marker')

    for marker, group in grouped:
        # Sélect 10 dernières lignes/valeurs pour chaque marqueur
        last_10_rows = group.tail(10)
        #print(last_10_rows) # Verif 10 dernières valeurs de GT, Ieq, Iraw, PD, RT pour chaque marker
        
        # Calcul moyennes pour les colonnes GT, Ieq, Iraw, PD, RT  
        means_dict[marker] = {
            'GT': last_10_rows['GT'].mean(),
            'Ieq': last_10_rows['Ieq'].mean(),
            'Iraw': last_10_rows['Iraw'].mean(),
            'PD': last_10_rows['PD'].mean(),
            'RT': last_10_rows['RT'].mean()
        }

    return pd.DataFrame(means_dict).T  # .T --> transposition, plus facile à lire