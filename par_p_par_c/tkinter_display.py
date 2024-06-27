import tkinter as tk #(pour ouvrir fenêtre supplémentaire)
from tkinter import ttk


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

# Préparation des données pour affichage dans Tkinter
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

deltas_df = pd.DataFrame(deltas_list)