#coding: utf-8

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt  #pour rep histogramme

from data_processing_par_p_par_c import calculate_means, group_wells_by_patient
from plotting_par_p_par_c import plot_histograms
from delta_calculation_par_p_par_c import calculate_deltas_means_by_treatment
from table_par_p_par_c import table_delta_base, table_delta_calculated, adjust_column_width

#-------------------------------------------------------------------------------------------------
def main(filepath, output_folder, generate_table=True, generate_graph=True):
    # Chargement du fichier Excel
    df = pd.read_excel(filepath)
    df = df[df['Description'] != 'vide']

    # Générer les tables si demandé
    if generate_table:
        moyennes = calculate_means(df)
        grouped_wells = group_wells_by_patient(df)
        aggregated_conditions = calculate_deltas_means_by_treatment(df, grouped_wells, moyennes)

        # Générer le tableau de valeurs des deltas
        delta_table_base = table_delta_base(aggregated_conditions)
        delta_table_calculated = table_delta_calculated(aggregated_conditions)

        output_excel_path = os.path.join(output_folder, 'delta_tables.xlsx')
        # Sauvegarder les tables dans un fichier Excel
        with pd.ExcelWriter(output_excel_path) as writer:
            delta_table_base.to_excel(writer, sheet_name='Base Deltas')
            delta_table_calculated.to_excel(writer, sheet_name='Calculated Deltas and Rates')

        adjust_column_width(output_excel_path)
        #print(f"Tableau de données généré et sauvegardé dans {output_excel_path}.")

    # Générer les graphiques si demandé
    if generate_graph:
        if not generate_table:
            # Calculer les données pour le graphique si la table n'a pas été générée
            moyennes = calculate_means(df)
            grouped_wells = group_wells_by_patient(df)
            aggregated_conditions = calculate_deltas_means_by_treatment(df, grouped_wells, moyennes)

        # Générer les histogrammes pour chaque patient
        for patient, deltas in aggregated_conditions.items():
            fig, axs = plot_histograms(patient, deltas, df)

        # Chemin de sauvegarde pour chaque graphique
            output_graph_path = os.path.join(output_folder, f"histogram_{patient}.png")
            fig.savefig(output_graph_path)
            plt.close(fig)  # Fermer la figure après la sauvegarde pour libérer la mémoire

#       plt.show()
            #print(f"Graphique pour le patient {patient} sauvegardé dans {output_graph_path}..")



    #print("Fin du programme.")

if __name__ == "__main__":
    filepath = sys.argv[1]  # Chemin du fichier passé en argument
    output_folder = sys.argv[2]  # Chemin du dossier de sortie passé en argument
    generate_table = sys.argv[3].lower() == 'true'  # Générer les tables ou non
    generate_graph = sys.argv[4].lower() == 'true'  # Générer les graphiques ou non
    main(filepath, output_folder, generate_table, generate_graph)
