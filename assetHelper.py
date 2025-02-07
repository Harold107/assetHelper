import sys
import os
from importlib import reload

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

"""
Only for testing
"""
project_path = r"C:\Users\Aro\Documents\GitHub\assetHelper"
if project_path not in sys.path:
    sys.path.append(project_path)
import settingDialog
reload(settingDialog)



def maya_main_window():
    # Return maya main window for parenting
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class AssetHelperDialog(QtWidgets.QDialog):

    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;ALL Files (*.*)"
    selected_filter = "Maya (*.ma *.mb)"
    selected_files_path = []
    # file_list = []



    def __init__(self, parent=maya_main_window()):
        super(AssetHelperDialog, self).__init__(parent)

        self.setWindowTitle("Asset Helper")
        self.setMinimumWidth(350)
        self.setMinimumHeight(500)
        # Remove HelpButton on the bar, check for python version
        if sys.version_info.major >= 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.import_assets_btn = QtWidgets.QPushButton("Import")
        self.remove_assets_btn = QtWidgets.QPushButton("Remove")
        self.info_btn = QtWidgets.QPushButton("Info")
        self.setting_btn = QtWidgets.QPushButton("Setting")

        self.preview_list = QtWidgets.QListWidget()
        self.preview_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # self.preview_list.addItem("Item 01")

        self.import_btn = QtWidgets.QPushButton("Import to Current Scene")
        self.import_btn.setFixedSize(150,30)
        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setFixedSize(50,30)


    def create_layouts(self):
        
        tool_bar_layout = QtWidgets.QHBoxLayout()
        tool_bar_layout.addWidget(self.import_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.remove_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.info_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.setting_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.close_btn)
        #, alignment=QtCore.Qt.AlignRight

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(tool_bar_layout)
        main_layout.addWidget(self.preview_list)
        main_layout.addLayout(button_layout)


    def create_connections(self):
        self.import_assets_btn.clicked.connect(self.open_import_dialog)
        self.remove_assets_btn.clicked.connect(self.remove_selected_item)
        self.info_btn.clicked.connect(self.open_info_dialog)
        self.setting_btn.clicked.connect(self.open_setting_dialog)
        self.close_btn.clicked.connect(self.close)


    def open_import_dialog(self, *arg):
        selected_files_path = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        if not selected_files_path[0]: 
            print("empty")
            return
        file_list = []
        for file in selected_files_path[0]:
            file_list.append((os.path.splitext(os.path.basename(file))[0]))
            print(os.path.splitext(os.path.basename(file))[0])

        # self.preview_list.addItems(['item1','item2'])


    def remove_selected_item(self):
        print("Remove item")


    def open_info_dialog(self):
        geo_info = "Asset Name: Cube\nPolycount: 100,00\nDate Modified: 2/1/2025"
        info_dialog = QtWidgets.QMessageBox.information(self, "Asset Information", geo_info)


    def open_setting_dialog(self):
        setting_dialog = settingDialog.SettingDialog(self)
        setting_dialog.show()

    def asset_to_list(self):
        pass



if __name__ == "__main__":
    try:
        asset_helper_dialog.close() # pylint: disable=E0601
        asset_helper_dialog.deleteLater()
    except:
        pass

    asset_helper_dialog = AssetHelperDialog()
    asset_helper_dialog.show()