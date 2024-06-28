import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  #pour rep histogramme
from data_processing import group_wells_by_patient


#avec seaborn
sns.set_style('darkgrid', {'grid.linestyle': '--'})

colors = sns.color_palette("tab10", 8)
units = {'GT': 'GT(mSiemens)', 'Ieq': 'Ieq(μA.cm²)', 'Iraw': 'Iraw(μA.cm²)', 'PD': 'PD(μV)', 'RT': 'RT(kΩ.cm²)'}

def plot_histograms(patient, deltas, df):
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


