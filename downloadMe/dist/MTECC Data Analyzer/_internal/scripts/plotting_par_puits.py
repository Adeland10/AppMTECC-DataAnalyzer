import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# Représentation des deltas --> Test 1 : HISTOGRAMME pour chaque puits avec 5 histogrammes pour chaque puit, un pour chaque mesure

# avec seaborn
sns.set_style('darkgrid', {'grid.linestyle': '--'})
colors = sns.color_palette("tab10", 8)
units = {'GT': 'GT(mSiemens)', 'Ieq': 'Ieq(μA.cm²)', 'Iraw': 'Iraw(μA.cm²)', 'PD': 'PD(μV)', 'RT': 'RT(kΩ.cm²)'}
measures = ['GT', 'Ieq', 'Iraw', 'PD', 'RT']
delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP', 'ΔFsk + ΔVX770', 'ΔFsk + ΔVX770 + ΔApi']

def plot_histo_par_puits(deltas_par_puits):
    figs ={}

    for well, deltas in deltas_par_puits.items():
        fig, axs = plt.subplots(5, 1, figsize=(10, 15))
        fig.suptitle(f'Deltas pour le puit {well}', fontsize=16)
        
        for i, measure in enumerate(measures):
            data_list = []
            for delta_name in delta_names:
                if measure in deltas.get(delta_name, {}):  # Vérifie si la mesure existe dans le delta_name
                    data_list.append({'Delta': delta_name, 'Value': deltas[delta_name][measure]})
                elif delta_name == 'ΔFsk + ΔVX770':
                    delta_fsk_vx770 = deltas.get('ΔFsk/IBMX', {}).get(measure, 0) + deltas.get('ΔVX770', {}).get(measure, 0)
                    data_list.append({'Delta': delta_name, 'Value': delta_fsk_vx770})
                elif delta_name == 'ΔFsk + ΔVX770 + ΔApi':
                    delta_fsk_vx770_api = delta_fsk_vx770 + deltas.get('ΔApi', {}).get(measure, 0)
                    data_list.append({'Delta': delta_name, 'Value': delta_fsk_vx770_api})
            
            data = pd.DataFrame(data_list)
            
            if not data.empty:
                sns.histplot(data=data, x='Delta', weights='Value', multiple='dodge', ax=axs[i], color=colors[i])
                axs[i].set_ylabel(units[measure], fontsize=9)
                axs[i].set_xlabel('Delta', fontsize=9)
                axs[i].tick_params(axis='x', rotation=0, labelsize=8)
        

        fig.tight_layout(rect=[0, 0, 1, 0.96])
        fig.subplots_adjust(hspace=0.5)
        figs[well]=fig

   # plt.show()  # Bloque jusqu'à ce que la fenêtre se ferme

    return figs