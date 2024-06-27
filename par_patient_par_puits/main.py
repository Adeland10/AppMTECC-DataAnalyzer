#coding: utf-8

import pandas as pd
import tkinter as tk #(pour ouvrir fenêtre supplémentaire)
from tkinter import ttk
from data_processing import calculate_means, calculate_delta_by_patient, group_wells_by_patient
from plotting import plot_histograms
from tkinter_display import show_dataframe

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

# Calculer les moyennes des 10 dernières valeurs par marqueur
moyennes = calculate_means(df)

# Calculer les deltas
deltas_par_patient = calculate_delta_by_patient(df, moyennes)
#print("Deltas entre les marqueurs successifs pour chaque patient :")
 #print(pd.DataFrame(deltas_par_patient)) #VERIF


plot_histograms(patient, deltas)

show_dataframe(deltas_df)

print("Fin du programme.")