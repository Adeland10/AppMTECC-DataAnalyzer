#coding: utf-8

import pandas as pd
import openpyxl as xl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt  #pour rep histogramme

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
df = df[df['Description'] != 'vide'] # Filtrer les puits non vides

grouped = df.groupby('Marker') # groupby() de pandas pour regrouper par Marker


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue pour les colonnes GT, Ieq, Iraw, PD, RT  

def calculate_means(df):
    means_dict = {}     # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur

    for marker, group in grouped:
        last_10_rows = group.tail(10)         # Sélect 10 dernières lignes/valeurs pour chaque marqueur
        print(last_10_rows) # Verif 10 dernières valeurs de GT, Ieq, Iraw, PD, RT pour chaque marker
        
        means_dict[marker] = {
            'GT': last_10_rows['GT'].mean(),
            'Ieq': last_10_rows['Ieq'].mean(),
            'Iraw': last_10_rows['Iraw'].mean(),
            'PD': last_10_rows['PD'].mean(),
            'RT': last_10_rows['RT'].mean()
        }

    return pd.DataFrame(means_dict).T  # .T --> transposition, plus facile à lire

#-------------------------------------------------------------------------------------------------
# Fonction pour regrouper les puits par patient

def group_wells_by_patient(df):
    patient_wells = {1: ['A1', 'B1', 'A2', 'B2', 'C1', 'C2', 'D1', 'D2'],
                     2: ['A3', 'A4', 'B3', 'B4', 'C3', 'C4', 'D3', 'D4'],
                     3: ['A5', 'A6', 'B5', 'B6', 'C5', 'C6', 'D5', 'D6']}

    grouped_patients = {}
    for patient, wells in patient_wells.items():
        valid_wells = [well for well in wells if well in df['Well'].values]
        if valid_wells:
            grouped_patients[patient] = valid_wells

    return grouped_patients

print(group_wells_by_patient(df)) #VERIFFFF

#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit en les regroupant par patients 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']

def calculate_delta_by_patient(df, means_df):
    all_deltas = {}
    patient_wells = group_wells_by_patient(df)

    for patient, wells in patient_wells.items():
        deltas = {}
        markers = sorted(means_df.index) #trier marker en ordre croissant pour calculer deltas de manière séquentielle entre les marqueurs
        delta_index = 0
    
        for i in range(1, len(markers)):
            marker1 = markers[i]
            marker0 = markers[i - 1]
            delta_name = delta_names[delta_index] if delta_index < len(delta_names) else f"Δ{marker0}-{marker1}"
            
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

        all_deltas[patient] = deltas  #stocker les données pour un patient
    
    return all_deltas

#-------------------------------------------------------------------------------------------------
# Calculer les moyennes des 10 dernières valeurs par marqueur
moyennes = calculate_means(df)
"""
print("Moyennes des 10 dernières valeurs par marqueur :")
print(moyennes)
"""
# Calculer les deltas
deltas_par_patient = calculate_delta_by_patient(df, moyennes)
#print("Deltas entre les marqueurs successifs pour chaque patient :")
"""
for well, deltas in deltas_par_puits.items():
    print(f"Puits {well} :")
    for delta_name, delta_values in deltas.items():
        print(f"{delta_name}: {delta_values}")
"""
print(pd.DataFrame(deltas_par_patient)) #VERIF

#-------------------------------------------------------------------------------------------------
# Représentation des deltas --> Test 1 : HISTOGRAMME pour chaque patient (delta = moyenne des 8 puits d'un patient)

#avec Matplotlib
"""
def plot_deltas_histograms(deltas_par_puits):
    delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
    colors = {'GT': 'blue', 'Ieq': 'green', 'Iraw': 'orange', 'PD': 'red', 'RT': 'purple'}

    # Parcourir chaque puits et créer un histogramme pour chaque type de delta
    for well, deltas in deltas_par_puits.items():
        fig, axs = plt.subplots(5, 1, figsize=(10, 20), sharex=True)

        # Pour chaque mesure (GT, Ieq, Iraw, PD, RT)
        for i, measure in enumerate(['GT', 'Ieq', 'Iraw', 'PD', 'RT']):
            values = []
            for delta_name in delta_names:
                values.append(deltas[delta_name][measure])

            values_log = np.log10(np.abs(values) + 1e-10)  # convertir en log et 1e-10 pour pas avoir log(0)
            # Barres de l'histogramme en échelle log
            x = np.arange(len(delta_names))
            axs[i].bar(x, values_log, color=colors[measure])
            axs[i].set_ylabel(measure + ' (log scale)')
            axs[i].set_xticks(x)
            axs[i].set_xticklabels(delta_names)
            axs[i].set_title(f"{well}: {measure} Delta Histogram (log scale)")
        
        plt.tight_layout()
        plt.show() # Bloque jusqu'à ce que la fenêtre soit fermée
        break
#plot_deltas_histograms(deltas_par_puits)
"""

#avec seaborn
sns.set_style('darkgrid', {'grid.linestyle': '--'})

colors = {'GT': 'blue', 'Ieq': 'green', 'Iraw': 'orange', 'PD': 'red', 'RT': 'purple'}
units = {'GT': 'mSiemens', 'Ieq': 'μA.cm²', 'Iraw': 'μA.cm²', 'PD': 'μV', 'RT': 'kΩ.cm²'}

for patient, deltas in deltas_par_patient.items():
    fig, axs = plt.subplots(5, 1, figsize=(6, 8))
    fig.suptitle(f'Deltas pour le patient {patient}', fontsize=15)  # Titre principal


    measures = ['GT', 'Ieq', 'Iraw', 'PD', 'RT']
    data_list = []
    
    for delta_name, delta_values in deltas.items():
        for key, value in delta_values.items():
            data_list.append({'Delta': delta_name, 'Type': key, 'Value': value, 'Patient': patient})

    data = pd.DataFrame(data_list)  # Créer le DataFrame une fois la liste complète
    
    for i, measure in enumerate(measures):
        measure_data = data[data['Type'] == measure]
        if not measure_data.empty:
            sns.histplot(data=measure_data, x='Delta', weights='Value', hue='Type', multiple='stack', shrink=0.25, ax=axs[i], palette=[colors[measure]])
            #axs[i].set_title(f'{measure} Deltas pour le patient {patient}')
            axs[i].set_xlabel('Delta',fontsize = 6)
            axs[i].set_ylabel([units[measure]], fontsize = 6)
            axs[i].set_xticks(np.arange(len(delta_names)))
            axs[i].set_xticklabels(delta_names, rotation=0)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Ajuste l'espacement pour le titre principal

plt.tight_layout()
plt.subplots_adjust(hspace=0.5)
plt.show()

print("Fin du programme.")

