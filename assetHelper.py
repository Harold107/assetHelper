import sys
import os
from importlib import reload

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

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
    # Class level variable
    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;ALL Files (*.*)"
    selected_filter = "Maya (*.ma *.mb)"
    selected_file_paths = []
    load_file_list = []
    hilight_index = None


    def __init__(self, parent=maya_main_window()):
        super(AssetHelperDialog, self).__init__(parent)
        # Set window value
        self.setWindowTitle("Asset Helper")
        self.setMinimumWidth(350)
        self.setMinimumHeight(500)
        # Remove HelpButton on the bar, check for python version
        if sys.version_info.major >= 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # Call all the methods for UI
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    # Create all the widgets
    def create_widgets(self):
        # Top bar widgets
        self.import_assets_btn = QtWidgets.QPushButton("Load")
        self.remove_assets_btn = QtWidgets.QPushButton("Remove")
        self.info_btn = QtWidgets.QPushButton("Info")
        self.setting_btn = QtWidgets.QPushButton("Setting")
        # Preview widget
        self.preview_list = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        self.preview_list.setModel(self.model)
        self.preview_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # Buttom widgets
        self.import_btn = QtWidgets.QPushButton("Import to Current Scene")
        self.import_btn.setFixedSize(150,30)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setFixedSize(50,30)

    # Create UI layouts and add widgets to respective layout
    def create_layouts(self):
        # Top buttons layout
        tool_bar_layout = QtWidgets.QHBoxLayout()
        tool_bar_layout.addWidget(self.import_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.remove_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.info_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.setting_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addStretch()
        # Buttom buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.close_btn)
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(tool_bar_layout)
        main_layout.addWidget(self.preview_list)
        main_layout.addLayout(button_layout)

    # Create connection between UI and function
    def create_connections(self):
        self.import_assets_btn.clicked.connect(self.open_import_dialog)
        self.remove_assets_btn.clicked.connect(self.remove_selected_item)
        self.info_btn.clicked.connect(self.open_info_dialog)
        self.setting_btn.clicked.connect(self.open_setting_dialog)
        self.import_btn.clicked.connect(self.import_to_scene)
        self.preview_list.clicked.connect(self.highlight_item)
        # self.model.itemChanged.connect(self.add_selected_to_list)
        self.close_btn.clicked.connect(self.test_print)

    # Functions for UI behavior
    def open_import_dialog(self, *arg):
        self.selected_file_paths = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", "", self.FILE_FILTERS, self.selected_filter)[0]
        # If cancel 
        if not self.selected_file_paths: 
            print("Cancel Select File Window")
            return
        # Get all asset name in file_list
        file_list = []
        for file in self.selected_file_paths:
            file_list.append((os.path.splitext(os.path.basename(file))[0]))

        # Add file name to preview
        self.asset_to_list(file_list)


    def remove_selected_item(self):
        self.model.removeRows(self.hilight_index.row(),1)


    def open_info_dialog(self):
        geo_info = "Asset Name: Cube\nPolycount: 100,00\nDate Modified: 2/1/2025"
        info_dialog = QtWidgets.QMessageBox.information(self, "Asset Information", geo_info)


    def open_setting_dialog(self):
        setting_dialog = settingDialog.SettingDialog(self)
        setting_dialog.show()


    def import_to_scene(self):
        if not self.model.rowCount():
            selection_warning_dialog = QtWidgets.QMessageBox.warning(self, "Import Asset Warning","No Asset Selected!\nPlease select at least one asset")
        # Iterate through the model
        for index in range(self.model.rowCount()):
            # Append to load_file_list if it's checked and not in list yet
            if self.model.item(index).checkState() == QtCore.Qt.CheckState.Checked:
                if self.model.item(index).text() not in self.load_file_list:
                    self.load_file_list.append(self.model.item(index).text())
            else:
                if self.model.item(index).text() in self.load_file_list:
                    self.load_file_list.remove(self.model.item(index).text())
        # Import file
        for path in self.selected_file_paths:
            cmds.file(path, i=True, ignoreVersion=True)


    def asset_to_list(self, file_list):
        for i in file_list:
            item = QtGui.QStandardItem(i)
            font = QtGui.QFont("Times", 15)
            item.setFont(font)
            item.setEditable(False)
            item.setCheckable(True) # not use checkable for selection for now
            self.model.appendRow(item)


    def highlight_item(self, index):
        self.hilight_index = index


    def test_print(self):
        print(self.selected_file_paths)





if __name__ == "__main__":
    try:
        asset_helper_dialog.close() # pylint: disable=E0601
        asset_helper_dialog.deleteLater()
    except:
        pass

    asset_helper_dialog = AssetHelperDialog()
    asset_helper_dialog.show()