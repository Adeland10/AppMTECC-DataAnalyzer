#coding utf-8

#TESTS



#----------------------------------------------------------------------
#Créer une Application avec une Boîte de Dialogue de Sélection de Fichier :

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface de Recherche Biologique")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.button = QPushButton("Sélectionner un fichier")
        self.button.clicked.connect(self.select_file)
        layout.addWidget(self.button)

        self.label = QLabel("Aucun fichier sélectionné")
        layout.addWidget(self.label)

        self.button = QPushButton("Exécuter le Code")
        self.button.clicked.connect(self.run_code)
        layout.addWidget(self.button)

        self.central_widget.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*);;Fichiers texte (*.txt)", options=options)
        if file_path:
            self.label.setText(f"Fichier sélectionné : {file_path}")
            # Appeler ton code de traitement de fichier ici, par exemple :
            # result = ton_module_python.ta_fonction(file_path)
            # Afficher ou traiter le résultat selon les besoins

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

#----------------------------------------------------------------------

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface de Recherche Biologique")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.button = QPushButton("Sélectionner un fichier")
        self.button.clicked.connect(self.select_file)
        layout.addWidget(self.button)

        self.label = QLabel("Aucun fichier sélectionné")
        layout.addWidget(self.label)

        self.run_button = QPushButton("Exécuter le Code")
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        self.central_widget.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*)", options=options)
        if file_name:
            self.label.setText(f"Fichier sélectionné: {file_name}")
        else:
            self.label.setText("Aucun fichier sélectionné")

    def run_code(self):
        # Code à exécuter lorsque le bouton "Exécuter le Code" est cliqué
        print("Code exécuté!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

#----------------------------------------------------------------------

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate table of data and graph")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        
        # Logo
        logo = QLabel(self)
        pixmap = QPixmap("inem_institut_necker_enfants_malades_logo.jpeg")
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo)
        
        # File Name Row
        file_layout = QHBoxLayout()
        file_label = QLabel("File name", self)
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        file_button = QPushButton("Select file", self)
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
        
        central_widget.setLayout(main_layout)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def select_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            self.folder_input.setText(folder_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






#coding utf-8

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QComboBox, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate table of data and graph")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon("inem_institut_necker_enfants_malades_logo.jpeg"))

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

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
        folder_label = QLabel("Output Folder",self)
        self.folder_input = QLineEdit(self)
        self.folder_input.setReadOnly(True)
        folder_button = QPushButton("Select Folder",self)
        folder_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(folder_button)

        main_layout.addLayout(folder_layout)

        #logo
        logo_layout = QHBoxLayout()
        logo = QLabel(self)
        pixmap = QPixmap("inem_institut_necker_enfants_malades_logo.jpeg")
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        logo_layout.addWidget(logo)


        logo_layout.addStretch()     # Spacer to align logo to the left

        main_layout.addWidget(logo)

        central_widget.setLayout(main_layout)

    
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)
        
    def select_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            self.folder_input.setText(folder_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



