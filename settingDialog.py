import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    # Return maya main window for parenting
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class SettingDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(SettingDialog, self).__init__(parent)

        self.setWindowTitle("Setting Window")
        self.setMinimumWidth(300)
        self.setMinimumHeight(150)
        self.setMaximumWidth(300)
        self.setMaximumHeight(150)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton()
        self.select_file_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_file_path_btn.setToolTip("Select File")

        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["Image View", "Text View"])

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")


    def create_layouts(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_file_path_btn)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("File:", file_path_layout)
        form_layout.addRow("View Style:", self.combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)


    def create_connections(self):
        self.select_file_path_btn.clicked.connect(self.add_default_dir)

        self.combobox.activated.connect(self.on_activated_int)
        self.combobox.activated[str].connect(self.on_activated_str) # [str] pyside handles it with the matching decorator

        self.apply_btn.clicked.connect(self.apply_setting)
        self.close_btn.clicked.connect(self.close)


    def add_default_dir():
        print("Open Folder Dialog")

    @QtCore.Slot(int)
    def on_activated_int(self, index):
        print(f"ComboBox Index: {index}")

    @QtCore.Slot(str)
    def on_activated_str(self, text):
        print(f"ComboBox Text: {text}")

    def apply_setting():
        print("Apply Default Dir")