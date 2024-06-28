import pandas as pd

from data_processing import group_wells_by_patient

#-------------------------------------------------------------------------------------------------
# Fonction pour calculer les deltas entre les marqueurs successifs de chaque puit en les regroupant par patients 

delta_names = ['ΔAmi', 'ΔFsk/IBMX', 'ΔVX770', 'ΔApi', 'ΔInh', 'ΔATP']

def calculate_delta_by_patient(df, means_dict):
    patient_wells = group_wells_by_patient(df)
    all_deltas = {}

    for patient, wells in patient_wells.items():
        deltas = {delta: {measure: [0] * len(wells) for measure in ['GT', 'Ieq', 'Iraw', 'PD', 'RT']} for delta in delta_names}
        for well_index, well in enumerate(wells):
            if well in means_dict:
                well_means = means_dict[well]
                markers = sorted(well_means.keys())
    
                for i in range(1, len(markers)):
                    marker1 = markers[i]
                    marker0 = markers[i - 1]
                    delta_name = delta_names[i-1]
                    
                    delta_GT = well_means[marker1]['GT'] - well_means[marker0]['GT']
                    delta_Ieq = well_means[marker1]['Ieq'] - well_means[marker0]['Ieq']
                    delta_Iraw = well_means[marker1]['Iraw'] - well_means[marker0]['Iraw']
                    delta_PD = well_means[marker1]['PD'] - well_means[marker0]['PD']
                    delta_RT = well_means[marker1]['RT'] - well_means[marker0]['RT']
                    
                    deltas[delta_name]['GT'][well_index] = delta_GT
                    deltas[delta_name]['Ieq'][well_index] = delta_Ieq
                    deltas[delta_name]['Iraw'][well_index] = delta_Iraw
                    deltas[delta_name]['PD'][well_index] = delta_PD
                    deltas[delta_name]['RT'][well_index] = delta_RT

        all_deltas[patient] = deltas #stocker les données pour un patient
    return all_deltas


#-------------------------------------------------------------------------------------------------
# fonction pour préparation des données pour affichage dans Tkinter

"""
def prepare_deltas_df(df, deltas_par_patient):
    deltas_list = []
    for patient, deltas in deltas_par_patient.items():
        for delta_name, measures in deltas.items():
            for measure, values in measures.items():
                for well_index, value in enumerate(values):
                    deltas_list.append({
                        'Patient': patient,
                        'Delta': delta_name,
                        'Measure': measure,
                        'Well': group_wells_by_patient(df)[patient][well_index],
                        'Value': round(value, 3)
                    })
    return pd.DataFrame(deltas_list)


#-------------------------------------------------------------------------------------------------
# Fonction pour afficher le DataFrame dans une fenêtre Tkinter

def show_dataframe(df):
    root = tk.Tk()
    root.title("Deltas DataFrame")
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor = 'center')
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    root.mainloop()
"""