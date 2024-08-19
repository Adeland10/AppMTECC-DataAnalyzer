#coding utf-8

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
        self.lineEdit().setPlaceholderText("None")
        self.view().pressed.connect(self.handleItemPressed)
        

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
            display_text = "None"
        self.lineEdit().setText(display_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate table of data and graph")
        self.setGeometry(100, 100, 800, 400)

        self.setWindowIcon(QIcon("inem_institut_necker_enfants_malades_logo.jpeg"))

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
        generate_button_layout.addWidget(generate_button)

        main_layout.addLayout(generate_button_layout)

        # Logo Layout
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)  # Align logo to the right and top
        logo = QLabel(self)
        pixmap = QPixmap("inem_institut_necker_enfants_malades_logo.jpeg")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
