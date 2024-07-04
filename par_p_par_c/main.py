#coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt  #pour rep histogramme
from data_processing import calculate_means, parse_description, group_wells_by_patient
from plotting import plot_histograms
from delta_calculation import calculate_deltas_means_by_treatment, calculate_delta_by_well, create_delta_table #show_dataframe, prepare_deltas_df

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

# Identifier les patients
#patient_dict = identify_patients(df['Description'])

#grouper les puits par patient 
grouped_wells = group_wells_by_patient(df)

#Calculer les deltas par traitement
aggregated_conditions = calculate_deltas_means_by_treatment(df, grouped_wells, moyennes)

 # Générer le tableau de valeurs des deltas
delta_table = create_delta_table(aggregated_conditions)
delta_table.to_excel('delta_table.xlsx')


#plt.ion() #mode intéractif ON
for patient, deltas in aggregated_conditions.items():
    plot_histograms(patient, deltas, df)

#plt.ioff()
plt.show()

#show_dataframe(deltas_df)

print("Fin du programme.")