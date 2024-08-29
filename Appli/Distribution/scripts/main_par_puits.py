import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

from data_processing_par_puits import calculate_means_by_well
from delta_calculation_par_puits import calculate_delta_by_well
from plotting_par_puits import plot_histo_par_puits
from table_par_puits import create_delta_table


def main(filepath, output_folder, generate_table=True, generate_graph=True):
    # Chargement du fichier Excel
    df = pd.read_excel(filepath)
    df = df[df['Description'] != 'vide']

    # Générer les tables si demandé
    if generate_table:
        moyennes = calculate_means_by_well(df)
        deltas_par_puits = calculate_delta_by_well(df, moyennes)
        
        delta_table = create_delta_table(deltas_par_puits)

        output_excel_path = os.path.join(output_folder, 'delta_table.xlsx')
        delta_table.to_excel(output_excel_path)
        #print(f"Tableau de données généré et sauvegardé dans {output_excel_path}.")

    # Générer les graphiques si demandé
    if generate_graph:
        if not generate_table:
            # Calculer les données pour le graphique si la table n'a pas été générée
            moyennes = calculate_means_by_well(df)
            deltas_par_puits = calculate_delta_by_well(df, moyennes)
        
        figs = plot_histo_par_puits(deltas_par_puits)

        for well, fig in figs.items():
            output_graph_path = os.path.join(output_folder, f'histogram_by_well_{well}.png')
            fig.savefig(output_graph_path)
            plt.close(fig)  # Fermer la figure après la sauvegarde pour libérer la mémoire

            #print(f"Graphique pour le puits {well} généré et sauvegardé dans {output_graph_path}.")



    #print("Fin du programme.")


if __name__ == "__main__":
    filepath = sys.argv[1]  # Chemin du fichier passé en argument
    output_folder = sys.argv[2]  # Chemin du dossier de sortie passé en argument
    generate_table = sys.argv[3].lower() == 'true'  # Générer les tables ou non
    generate_graph = sys.argv[4].lower() == 'true'  # Générer les graphiques ou non
    main(filepath, output_folder, generate_table, generate_graph)