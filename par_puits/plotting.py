import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Représentation des deltas --> Test 1 : HISTOGRAMME pour chaque puits avec 5 histogrammes pour chaque puit, un pour chaque mesure

#avec seaborn
sns.set_style('darkgrid', {'grid.linestyle': '--'})
colors = sns.color_palette("tab10", 8)
units = {'GT': 'GT(mSiemens)', 'Ieq': 'Ieq(μA.cm²)', 'Iraw': 'Iraw(μA.cm²)', 'PD': 'PD(μV)', 'RT': 'RT(kΩ.cm²)'}
measures = ['GT', 'Ieq', 'Iraw', 'PD', 'RT']

def plot_histo_par_puits(deltas_par_puits):
    for well, deltas in deltas_par_puits.items():
        fig, axs = plt.subplots(5, 1, figsize=(10, 15))
        fig.suptitle(f'Deltas pour le puit {well}', fontsize=16)
        
        for i, measure in enumerate(measures):
            data_list = []
            for delta_name, delta_values in deltas.items():
                data_list.append({'Delta': delta_name, 'Value': delta_values[measure]})
            
            data = pd.DataFrame(data_list)
            
            if not data.empty:
                sns.histplot(data=data, x='Delta', weights='Value', multiple='dodge', ax=axs[i], color=colors[i])
                axs[i].set_ylabel(units[measure], fontsize=9)
                axs[i].set_xlabel('Delta', fontsize=9)
                axs[i].tick_params(axis='x', rotation=0, labelsize=8)
        
        fig.canvas.manager.set_window_title(f"Puits {well}")
        
        if well == 'D6':
            def on_close(event):
                plt.close('all')  # Ferme toutes les fenêtres

            fig.canvas.mpl_connect('close_event', on_close)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.subplots_adjust(hspace=0.5)
    plt.show() #bloque jusqu'à ce que la fenêtre se ferme 
