#coding utf-8

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt



class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().clear()
        self.view().pressed.connect(self.handleItemPressed)
        self.updateDisplayText()  # Assurez-vous que le texte est vide au démarrage

    def addItem(self, text):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def itemChecked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == Qt.Checked

    def checkedItems(self):
        checked_items = []
        for index in range(self.model().rowCount()):
            if self.itemChecked(index):
                checked_items.append(self.model().item(index, 0).text())
        return checked_items

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
            
        self.updateNoneItem()
        self.updateDisplayText()


    def updateNoneItem(self):
        # "None" is the first item
        none_item = self.model().item(0)
        if self.itemChecked(0):
            for index in range(1, self.model().rowCount()):
                item = self.model().item(index, 0)
                item.setCheckState(Qt.Unchecked)
        else:
            if not any(self.itemChecked(index) for index in range(1, self.model().rowCount())):
                none_item.setCheckState(Qt.Checked)

    def updateDisplayText(self):
        checked_items = self.checkedItems()
        if checked_items:
            display_text = ", ".join(checked_items)
        else:
            display_text = "       "
        self.lineEdit().setText(display_text)

# Détermine le chemin de base
        if getattr(sys, 'frozen', False):
            # Chemin de l'exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Chemin du script Python
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        assets_path = os.path.join(base_path, 'assets')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTECC Data Analyzer")
        self.setGeometry(100, 100, 1000, 400)

        # Détermine le chemin de base
        if getattr(sys, 'frozen', False):
            # Chemin de l'exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Chemin du script Python
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        assets_path = os.path.join(base_path, 'assets')
        logo_path = os.path.join(assets_path, 'inem_institut_necker_enfants_malades_logo.jpeg')
        
        
        self.setWindowIcon(QIcon(logo_path))

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout that will contain all other layouts
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Minimal spacing between widgets

        # File Name Row
        file_layout = QHBoxLayout()
        file_label = QLabel("File Name", self)
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        file_button = QPushButton("Select File", self)
        file_button.clicked.connect(self.select_file)

        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)

        main_layout.addLayout(file_layout)

        # Output Folder Row
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Output Folder", self)
        self.folder_input = QLineEdit(self)
        self.folder_input.setReadOnly(True)
        folder_button = QPushButton("Select Folder", self)
        folder_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(folder_button)

        main_layout.addLayout(folder_layout)


        # Spacer to add space between Output Folder and Table of Data
        #spacer = QSpacerItem(10, 30)
        #main_layout.addItem(spacer)
        main_layout.addSpacing(30)


        # Table of Data Row
        table_layout = QHBoxLayout()
        table_label = QLabel("Table of data", self)

        self.table_combo = CheckableComboBox(self)
        self.table_combo.addItem("None")
        self.table_combo.addItem("Wells")
        self.table_combo.addItem("Patients")

        table_layout.addWidget(table_label)
        table_layout.addWidget(self.table_combo)

        main_layout.addLayout(table_layout)

        # Graph Row
        graph_layout = QHBoxLayout()
        graph_label = QLabel("Graph", self)
        
        self.graph_combo = CheckableComboBox(self)
        self.graph_combo.addItem("None")
        self.graph_combo.addItem("Well's histograms")
        self.graph_combo.addItem("Patient's histograms")

        graph_layout.addWidget(graph_label)
        graph_layout.addWidget(self.graph_combo)

        main_layout.addLayout(graph_layout)

        # Generate Button
        generate_button_layout = QHBoxLayout()
        generate_button_layout.setAlignment(Qt.AlignCenter)
        generate_button = QPushButton("Generate", self)
        generate_button.clicked.connect(self.generate_clicked)

        generate_button_layout.addWidget(generate_button)

        main_layout.addLayout(generate_button_layout)

        # Logo Layout
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)  # Align logo to the right and top
        logo = QLabel(self)
        # Détermine le chemin de base
        if getattr(sys, 'frozen', False):
            # Chemin de l'exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Chemin du script Python
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        assets_path = os.path.join(base_path, 'assets')
        logo_path = os.path.join(assets_path, 'inem_institut_necker_enfants_malades_logo.jpeg')

        pixmap = QPixmap(logo_path)
        logo.setPixmap(pixmap)
        logo_layout.addWidget(logo)

        # Top layout combining main layout and logo layout
        top_layout = QHBoxLayout()
        top_layout.addLayout(main_layout)
        top_layout.addLayout(logo_layout)

        # Set the layout of the central widget
        central_widget.setLayout(top_layout)


    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def select_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            self.folder_input.setText(folder_name)

    def handle_table_selection(self):
        # Déselectionne "None" si une autre option est sélectionnée
        selected_text = self.table_combo.currentText()
        if selected_text != "       ":
            self.table_combo.removeItem(0)

    def handle_graph_selection(self):
        # Déselectionne "None" si une autre option est sélectionnée
        selected_text = self.graph_combo.currentText()
        if selected_text != "       ":
            self.graph_combo.removeItem(0)


    def generate_clicked(self):
        filepath = self.file_input.text()
        output_folder = self.folder_input.text()

        selected_table_options = self.table_combo.checkedItems()
        selected_graph_options = self.graph_combo.checkedItems()

        # Appelle la fonction correspondante dans le fichier functions.py
        # En fonction des options sélectionnées
        from functions import execute_script, show_confirmation_message

        if selected_table_options or selected_graph_options:
            if "Wells" in selected_table_options or "Well's histograms" in selected_graph_options:
                execute_script(
                    "main_par_puits.py",
                    filepath,
                    output_folder,
                    "Wells" in selected_table_options,
                    "Well's histograms" in selected_graph_options
                )

        if "Patients" in selected_table_options or "Patient's histograms" in selected_graph_options:
            execute_script(
                "main_par_p_par_c.py",
                filepath,
                output_folder,
                "Patients" in selected_table_options,
                "Patient's histograms" in selected_graph_options
            )

        show_confirmation_message(output_folder)


