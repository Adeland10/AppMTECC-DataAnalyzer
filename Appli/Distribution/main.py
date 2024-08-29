#coding utf-8

import sys
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from functions import execute_script


def on_generate_clicked():
    filepath = MainWindow.file_input.text()  # Récupère le fichier sélectionné
    
    # Vérification des options sélectionnées dans les ComboBoxes
    selected_table_options = MainWindow.table_combo.currentData()
    selected_graph_options = MainWindow.graph_combo.currentData()
    
    # Logique pour déterminer quelles options sont sélectionnées
    generate_wells_data = "Wells" in selected_table_options if selected_table_options else False
    generate_patients_data = "Patients" in selected_table_options if selected_table_options else False
    generate_wells_histograms = "Well's histograms" in selected_graph_options if selected_graph_options else False
    generate_patients_histograms = "Patient's histograms" in selected_graph_options if selected_graph_options else False


    if generate_wells_data or generate_wells_histograms:
        execute_script(
            "main_par_puits.py",
            filepath,
            generate_wells_data,
            generate_wells_histograms
        )

    if generate_patients_data or generate_patients_histograms:
        execute_script(
            "main_par_p_par_c.py",
            filepath,
            generate_patients_data,
            generate_patients_histograms
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
