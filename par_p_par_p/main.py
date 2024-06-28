#coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt  #pour rep histogramme
from data_processing import calculate_means
from plotting import plot_histograms
from delta_calculation import calculate_delta_by_patient #show_dataframe, prepare_deltas_df

#-------------------------------------------------------------------------------------------------
#importation du fichier excel et de la fenêtre contenant les raw data
filepath = r'C:\Users\adele\Bureau\INEM\Code-MTECC\HNE PredictCFdec162k p1+3F508del and CastanierSoleneWT p1+3 and no cells in 5 6 20 06 24_comp.xlsx'
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

 # Préparer le dataframe pour l'affichage dans Tkinter
#deltas_df = prepare_deltas_df(df, deltas_par_patient)

#plt.ion() #mode intéractif ON
for patient, deltas in deltas_par_patient.items():
    plot_histograms(patient, deltas, df)

#plt.ioff()
plt.show()

#show_dataframe(deltas_df)

print("Fin du programme.")