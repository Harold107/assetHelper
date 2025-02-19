import sys
import os
import json
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
project_path = r"C:\Users\spike\Documents\GitHub\assetHelper"
if project_path not in sys.path:
    sys.path.append(project_path)
import settingDialog
reload(settingDialog)
import helperFunctions
reload(helperFunctions)



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
    JSON_PATH = os.path.dirname(os.path.abspath(__file__)) + r"\assetinfo.json"
    IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\image\\"
    selected_filter = "Maya (*.ma *.mb)"
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

        self.initialize_data()

    # Create all the widgets
    def create_widgets(self):
        # Top bar widgets
        self.import_assets_btn = QtWidgets.QPushButton("Load")
        self.remove_assets_btn = QtWidgets.QPushButton("Remove")
        self.info_btn = QtWidgets.QPushButton("Info")
        self.setting_btn = QtWidgets.QPushButton("Setting")
        self.reset_btn = QtWidgets  .QPushButton("Reset")

        # Preview widget
        self.preview_list = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        self.preview_list.setModel(self.model)
        self.preview_list.setIconSize(QtCore.QSize(180,180))
        # self.preview_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Buttom widgets
        self.import_btn = QtWidgets.QPushButton("Import to Current Scene")
        self.import_btn.setFixedSize(200,30)

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
        tool_bar_layout.addWidget(self.reset_btn, alignment=QtCore.Qt.AlignLeft)
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
        self.reset_btn.clicked.connect(self.reset_data)
        self.import_btn.clicked.connect(self.import_to_scene)
        self.preview_list.clicked.connect(self.highlight_item)
        self.close_btn.clicked.connect(self.test_print)

    # Functions for UI behavior
    def open_import_dialog(self, *arg):
        selected_file_paths = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", "", self.FILE_FILTERS, self.selected_filter)[0]

        # If cancel clicked
        if not selected_file_paths: 
            print("Cancel Select File Window")
            return

        # Get all asset name in asset_list
        asset_list = [] #list for all asset name
        path_list = [] #list for all path
        for file in selected_file_paths:
            asset_list.append((os.path.splitext(os.path.basename(file))[0]))
            path_list.append(file)

        # load files from path list
        for n in range (len(path_list)):
            helperFunctions.load_files(asset_list[n], path_list[n], self.JSON_PATH, self.IMAGE_PATH)

        # Add file name to preview
        self.asset_to_list(asset_list)


    def remove_selected_item(self):
        helperFunctions.delete_load_asset(self.model.itemFromIndex(self.hilight_index).text(), self.JSON_PATH, self.IMAGE_PATH)
        self.model.removeRow(self.hilight_index.row())


    def open_info_dialog(self):
        asset_name = self.model.itemFromIndex(self.hilight_index).text() # get asset name from clicked list item
        data_list = helperFunctions.get_asset_data(asset_name, self.JSON_PATH) # use asset name from json data

        geo_info = f"Asset Name: {asset_name}\nPolycount: {data_list[0]}\nDate Modified: {data_list[2]}" # store display message
        info_dialog = QtWidgets.QMessageBox.information(self, "Asset Information", geo_info)


    def open_setting_dialog(self):
        setting_dialog = settingDialog.SettingDialog(self)
        setting_dialog.show()


    def import_to_scene(self):
        selected_file_paths = [] # contain asset file paths
        load_file_list = [] # contain asset names
        if not self.model.rowCount():
            selection_warning_dialog = QtWidgets.QMessageBox.warning(self, "Import Asset Warning","No Asset Selected!\nPlease select at least one asset")

        # Iterate through the model
        for index in range(self.model.rowCount()):
            # Append to load_file_list if it's checked and not in list yet
            if self.model.item(index).checkState() == QtCore.Qt.CheckState.Checked:
                if self.model.item(index).text() not in load_file_list:
                    load_file_list.append(self.model.item(index).text())
            else:
                if self.model.item(index).text() in load_file_list:
                    load_file_list.remove(self.model.item(index).text())

        # Append file path to list 
        for asset in load_file_list:
            file_path = helperFunctions.get_asset_data(asset, self.JSON_PATH)[1]
            selected_file_paths.append(file_path)

        # Import file from the path list
        for path in selected_file_paths:
            cmds.file(path, i=True, ignoreVersion=True)


    def asset_to_list(self, asset_list):
        for asset_name in asset_list:
            item = QtGui.QStandardItem(asset_name) # set item name
            font = QtGui.QFont("Times", 15) # create item font
            item.setFont(font) # set font
            item.setIcon(QtGui.QIcon(self.IMAGE_PATH + asset_name + ".0.png")) # set image icon
            item.setEditable(False) # set not editable
            item.setCheckable(True) # not use checkable for selection for now
            self.model.appendRow(item) # add to listview


    def highlight_item(self, index):
        # set class variable input item index
        self.hilight_index = index


    def reset_data(self):
        json_data = [] # create empty list to replace json data
        if os.path.exists(self.JSON_PATH):
            with open(self.JSON_PATH, "w") as file:
                # dump empty data to json file
                json.dump(json_data, file, indent=4)

        self.model.clear() # clear list view

        # delete all images
        images = os.listdir(self.IMAGE_PATH)
        for image in images:
            os.remove(self.IMAGE_PATH + image)


    # initialize data when asset helper window created
    def initialize_data(self):
        asset_list = [] # list for reading in existing json data
        if os.path.exists(self.JSON_PATH):
            if os.stat(self.JSON_PATH).st_size != 0:
                with open(self.JSON_PATH, "r") as file:
                    json_data = json.load(file)
                # append json data to empty list
                for data in json_data:
                    asset_list.append(list(data.keys())[0])
            self.asset_to_list(asset_list)


    # test function
    def test_print(self):
        # print(self.selected_file_paths)
        print(self.JSON_PATH)





if __name__ == "__main__":
    try:
        asset_helper_dialog.close() # pylint: disable=E0601
        asset_helper_dialog.deleteLater()
    except:
        pass

    asset_helper_dialog = AssetHelperDialog()
    asset_helper_dialog.show()