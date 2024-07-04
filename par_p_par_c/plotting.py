import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  #pour rep histogramme


#avec seaborn
sns.set_style('darkgrid', {'grid.linestyle': '--'})

colors = sns.color_palette("tab10", 4)
units = {'GT': 'GT(mSiemens)', 'Ieq': 'Ieq(μA.cm²)', 'Iraw': 'Iraw(μA.cm²)', 'PD': 'PD(μV)', 'RT': 'RT(kΩ.cm²)'}
measures = ['GT', 'Ieq', 'Iraw', 'PD', 'RT']
#treatment_labels = {1: 'ctrl', 2: 'ctrl+VX770', 3: 'ctrl+vx770+Api', 4: 'vx661+vx445+vx770+Api', 5: 'vx661+vx445+vx770'}


def plot_histograms(patient, deltas, df):
    fig, axs = plt.subplots(5, 1, figsize=(10, 15))
    fig.suptitle(f'Deltas pour le patient {patient}', fontsize=15)  # Titre principal
        
    for i, measure in enumerate(measures):
        data_list = []
        for condition, condition_deltas in deltas.items():
            for delta_name, delta_values in condition_deltas.items():
                #print(f"Measure: {measure}")
                #print(f"Delta Values: {delta_values}")

            
                if isinstance(delta_values, dict) :
                    if measure in delta_values:
                        data_list.append({
                            'Delta': delta_name,
                            'Condition': f"{condition[0]}_{condition[1]}",
                            'Value': delta_values[measure]
                        })
                    else :
                        print(f"Warning: Measure '{measure}' not found in delta_values")
                else:
                    print(f"Warning: delta_values is not a dictionary, skipping")
        if data_list:
            data = pd.DataFrame(data_list)
            sns.barplot(data=data, x='Delta', y='Value', hue='Condition', ax=axs[i], palette=colors)
            axs[i].set_ylabel(units[measure], fontsize=9)
            axs[i].set_xlabel('Delta', fontsize=9)
            axs[i].tick_params(axis='x', labelrotation=0, labelsize=8)
            axs[i].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)  # Déplacer la légende à gauche
        else:
            print(f"No data to plot for measure '{measure}'")

        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.subplots_adjust(hspace=0.5)
    fig.canvas.manager.set_window_title(f"Patient {patient}")
    

