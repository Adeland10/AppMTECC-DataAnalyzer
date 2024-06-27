#coding: utf-8

import pandas as pd
import openpyxl as xl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt  #pour rep histogramme
import tkinter as tk #(pour ouvrir fenêtre supplémentaire)
from tkinter import ttk
import threading #pour ouvrir fenetre simultanement --> utiliser des threads

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

grouped = df.groupby(['Well', 'Marker']) # groupby() de pandas pour regrouper par Marker


#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les moyennes des dernières 
# valeurs d'un même marker avant l'ajout de la drogue pour les colonnes GT, Ieq, Iraw, PD, RT  

def calculate_means(df):
    means_dict = {}     # Initialisation dictionnaire pour stocker les moyennes des 10 dernières valeurs par colonne et par marqueur

    for (well, marker), group in grouped:
        last_10_rows = group.tail(10)         # Sélect 10 dernières lignes/valeurs pour chaque marqueur
        #print(last_10_rows) # Verif 10 dernières valeurs de GT, Ieq, Iraw, PD, RT pour chaque marker
        
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

#print(group_wells_by_patient(df)) #VERIFFFF

#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit en les regroupant par patients 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']
patient_wells = group_wells_by_patient(df)

def calculate_delta_by_patient(df, means_dict):
    all_deltas = {}

    for patient, wells in patient_wells.items():
        deltas = {delta: {measure: [0] * len(wells) for measure in ['GT', 'Ieq', 'Iraw', 'PD', 'RT']} for delta in delta_names}
        for well_index, well in enumerate(wells):
            if well in means_dict:
                well_means = means_dict[well]
                markers = sorted(well_means.keys())
    
                for i in range(1, len(markers)):
                    marker1 = markers[i]
                    marker0 = markers[i - 1]
                    delta_name = delta_names[i-1]
                    
                    delta_GT = well_means[marker1]['GT'] - well_means[marker0]['GT']
                    delta_Ieq = well_means[marker1]['Ieq'] - well_means[marker0]['Ieq']
                    delta_Iraw = well_means[marker1]['Iraw'] - well_means[marker0]['Iraw']
                    delta_PD = well_means[marker1]['PD'] - well_means[marker0]['PD']
                    delta_RT = well_means[marker1]['RT'] - well_means[marker0]['RT']
                    
                    deltas[delta_name]['GT'][well_index] = delta_GT
                    deltas[delta_name]['Ieq'][well_index] = delta_Ieq
                    deltas[delta_name]['Iraw'][well_index] = delta_Iraw
                    deltas[delta_name]['PD'][well_index] = delta_PD
                    deltas[delta_name]['RT'][well_index] = delta_RT

        all_deltas[patient] = deltas #stocker les données pour un patient
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
 #print(pd.DataFrame(deltas_par_patient)) #VERIF


#-------------------------------------------------------------------------------------------------
# Représentation des deltas --> Test 1 : HISTOGRAMME pour chaque patient avec deltas pour chaque 8 puits

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

colors = sns.color_palette("tab10", 8)
units = {'GT': 'GT(mSiemens)', 'Ieq': 'Ieq(μA.cm²)', 'Iraw': 'Iraw(μA.cm²)', 'PD': 'PD(μV)', 'RT': 'RT(kΩ.cm²)'}

def plot_histograms(patient, deltas):
    for patient, deltas in deltas_par_patient.items():
        fig, axs = plt.subplots(5, 1, figsize=(10, 15))
        fig.suptitle(f'Deltas pour le patient {patient}', fontsize=15)  # Titre principal
        measures = ['GT', 'Ieq', 'Iraw', 'PD', 'RT']
        
        for i, measure in enumerate(measures):
            data_list = []
            for delta_name, delta_values in deltas.items():
                for well_index, value in enumerate(delta_values[measure]):
                    data_list.append({'Delta': delta_name, 'Well': group_wells_by_patient(df)[patient][well_index], 'Value': value})
            data = pd.DataFrame(data_list)
            sns.barplot(data=data, x='Delta', y='Value', hue='Well', ax=axs[i], palette=colors)
            axs[i].set_ylabel(units[measure], fontsize=9)
            axs[i].set_xlabel('Delta', fontsize=9)
            axs[i].tick_params(axis='x', labelrotation=0, labelsize=8)
            axs[i].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)  # Déplacer la légende à gauche

        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.subplots_adjust(hspace=0.5)
        fig.canvas.manager.set_window_title(f"Patient {patient}")
        fig.show()


#-------------------------------------------------------------------------------------------------
# Fonction pour afficher le DataFrame dans une fenêtre Tkinter

"""
def show_dataframe(df):
    root = tk.Tk()
    root.title("Deltas DataFrame")
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    root.mainloop()

# Afficher le DataFrame dans une fenêtre Tkinter
deltas_df = pd.DataFrame(deltas_par_patient)
show_dataframe(deltas_df)
"""

def show_dataframe(df):
    root = tk.Tk()
    root.title("Deltas DataFrame")
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor = 'center')
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    root.mainloop()

# Préparation des données pour affichage dans Tkinter
deltas_list = []
for patient, deltas in deltas_par_patient.items():
    for delta_name, measures in deltas.items():
        for measure, values in measures.items():
            for well_index, value in enumerate(values):
                deltas_list.append({
                    'Patient': patient,
                    'Delta': delta_name,
                    'Measure': measure,
                    'Well': group_wells_by_patient(df)[patient][well_index],
                    'Value': round(value, 3)
                })

deltas_df = pd.DataFrame(deltas_list)



plot_histograms(patient, deltas)

show_dataframe(deltas_df)


print("Fin du programme.")






