#coding: utf-8

import pandas as pd
import openpyxl as xl

#-------------------------------------------------------------------------------------------------
#importation du fichier excel et de la fenêtre contenant les raw data
filepath = r'C:\Users\adele\Bureau\INEM\Code\HNE PredictCFdec162k p1+3F508del and CastanierSoleneWT p1+3 and no cells in 5 6 20 06 24_comp.xlsx'
sheet= 'HNE WT x3 IP FZ ISG sans grad e'
df = pd.read_excel(filepath, sheet)
print("fichier loaded") #vérif
print(df.head())        #vérif

""" DATA TEST """
df_test=df.head()


#-------------------------------------------------------------------------------------------------
#Création d'un dictionnaire pour chaque marker contenant les valeurs de Ieq, Iraw et GT correspondantes

marker_dict = {}    # Initialiser un dictionnaire vide pour stocker les listes dédiées
                    #où les clés sont les valeurs uniques de Marker et les valeurs 
                    #sont des listes contenant les lignes correspondantes

for index, row in df_test.iterrows():
    marker_value = row['Marker']
    if marker_value not in marker_dict:
        marker_dict[marker_value] = {'GT': [], 'Ieq': [], 'Iraw': [], 'PD': [], 'RT': []} # créer et initialiser les listes pour chaque marker
        print(marker_value)                                           # si la clé n'existe pas encore
    marker_dict[marker_value]['GT'].append(row['GT'])
    marker_dict[marker_value]['Ieq'].append(row['Ieq'])
    marker_dict[marker_value]['Iraw'].append(row['Iraw'])
    marker_dict[marker_value]['PD'].append(row['PD'])
    marker_dict[marker_value]['RT'].append(row['RT'])

"""" TEST CODE !!!!"""
for marker, values in marker_dict.items():
    print(f"Marker {marker}:")
    print(f"GT: {values['GT']}")
    print(f"Ieq: {values['Ieq']}")
    print(f"Iraw: {values['Iraw']}")
    print(f"PD: {values['PD']}")
    print(f"RT: {values['RT']}")
 

#-------------------------------------------------------------------------------------------------
#Définir une fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue

def calcul_delta(values_list):
    for marker, values_list in marker_dict.items():
        moyAvDrogue{marker} = mean(values_list[-3:])
        return moyAvDrogue{marker}
    
def calculate_means(df):
    grouped = df.groupby('Marker').mean()    # Utiliser groupby() de pandas pour regrouper par Marker et calculer les moyennes
    return grouped

# Calculer et afficher les moyennes des 3 dernières valeurs pour chaque marqueur
for marker, values in marker_dict.items():
    print(f"Marker {marker}:")
    print(f"GT (last 3 avg): {calcul_delta(values['GT'])}")
    print(f"Ieq (last 3 avg): {calcul_delta(values['Ieq'])}")
    print(f"Iraw (last 3 avg): {calcul_delta(values['Iraw'])}")
    print(f"PD (last 3 avg): {calcul_delta(values['PD'])}")
    print(f"RT (last 3 avg): {calcul_delta(values['RT'])}")