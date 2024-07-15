#coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt  #pour rep histogramme

from data_processing import calculate_means, group_wells_by_patient
from plotting import plot_histograms
from delta_calculation import calculate_deltas_means_by_treatment
from table import table_delta_base, table_delta_calculated, adjust_column_width


#-------------------------------------------------------------------------------------------------
#importation du fichier excel et de la fenêtre contenant les raw data
filepath = r'C:\Users\adele\Bureau\INEM\CODE\Code-MTECC\HNE Da Silva Ferreira Chloe p1+3 and Christofoli Regis p1+3 and Gualtieri Mathis p1+3 ctrl ETI 12 07 24_comp.xlsx'
sheet= 'HNE PredictCFdec162k p1+3F508de'
df = pd.read_excel(filepath)
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
delta_table_base = table_delta_base(aggregated_conditions)
delta_table_calculated = table_delta_calculated(aggregated_conditions)

# Save the delta tables to the same Excel file but on different sheets
with pd.ExcelWriter('delta_tables.xlsx') as writer:
    delta_table_base.to_excel(writer, sheet_name='Base Deltas')
    delta_table_calculated.to_excel(writer, sheet_name='Calculated Deltas and Rates')

adjust_column_width('delta_tables.xlsx')


#plt.ion() #mode intéractif ON

for patient, deltas in aggregated_conditions.items():
    plot_histograms(patient, deltas, df)

#plt.ioff()
plt.show()


print("Fin du programme.")