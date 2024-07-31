import pandas as pd

from data_processing import calculate_means_by_well
from delta_calculation import calculate_delta_by_well
from plotting import plot_histo_par_puits
from table import create_delta_table


filepath = r'C:\Users\adele\Bureau\INEM\CODE\Code-MTECC\ReadyToAnalyze\HNE PredictCFdec162k p1+3F508del and CastanierSoleneWT p1+3 and no cells in 5 6 20 06 24_comp.xlsx'
#sheet = 'HNE PredictCFdec162k p1+3F508de'
df = pd.read_excel(filepath)

df = df[df['Description'] != 'vide']

moyennes = calculate_means_by_well(df)
deltas_par_puits = calculate_delta_by_well(df, moyennes)
    
delta_table = create_delta_table(deltas_par_puits)
delta_table.to_excel('delta_table.xlsx')
    
plot_histo_par_puits(deltas_par_puits)
print("Fin du programme.")