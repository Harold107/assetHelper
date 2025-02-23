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
    ASSET_DIR = ""
    ICON_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\icon\\"
    JSON_PATH = os.path.dirname(os.path.abspath(__file__)) + r"\assetinfo.json"
    IMAGE_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\image\\"
    selected_filter = "Maya (*.ma *.mb)"
    hilight_index = None
    center_layout = None
    info_layout = None
    info_switch = False


    def __init__(self, parent=maya_main_window()):
        super(AssetHelperDialog, self).__init__(parent)
        # Set window value
        self.setWindowTitle("Asset Helper")
        self.setMinimumWidth(700)
        self.setMinimumHeight(810)
        self.setMaximumWidth(700)

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
        # Load button
        self.load_assets_btn = QtWidgets.QPushButton("")
        self.load_assets_btn.resize(QtCore.QSize(113, 41))
        self.load_assets_btn.setIcon(QtGui.QIcon(self.ICON_DIR + "load_icon.png"))
        self.load_assets_btn.setIconSize(QtCore.QSize(40, 40)) 
        self.load_assets_btn.setToolTip("Load Asset File\nLoad 3D asset to asset helper")
        # Remove button
        self.remove_assets_btn = QtWidgets.QPushButton("")
        self.remove_assets_btn.resize(QtCore.QSize(113, 41))
        self.remove_assets_btn.setIconSize(QtCore.QSize(40, 40)) 
        self.remove_assets_btn.setIcon(QtGui.QIcon(self.ICON_DIR + "remove_icon.png"))
        self.remove_assets_btn.setToolTip("Remove Asset\nRemove selected asset")
        # Info button
        self.info_btn = QtWidgets.QPushButton("")
        self.info_btn.resize(QtCore.QSize(113, 41))
        self.info_btn.setIconSize(QtCore.QSize(40, 40)) 
        self.info_btn.setIcon(QtGui.QIcon(self.ICON_DIR + "info_icon.png"))
        self.info_btn.setToolTip("Information\nDisplay selected asset info")
        # Setting button
        self.setting_btn = QtWidgets.QPushButton("")
        self.setting_btn.resize(QtCore.QSize(113, 41))
        self.setting_btn.setIconSize(QtCore.QSize(40, 40)) 
        self.setting_btn.setIcon(QtGui.QIcon(self.ICON_DIR + "setting_icon.png"))
        self.setting_btn.setToolTip("Setting\nShow the setting window for asset helper")
        # Reset button
        self.reset_btn = QtWidgets  .QPushButton("")
        self.reset_btn.resize(QtCore.QSize(113, 41))
        self.reset_btn.setIconSize(QtCore.QSize(40, 40)) 
        self.reset_btn.setIcon(QtGui.QIcon(self.ICON_DIR + "reset_icon.png"))
        self.reset_btn.setToolTip("Rest All Records\nReset all the current asset records and setting")

        # Preview widget
        self.preview_list = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        self.preview_list.setModel(self.model)
        self.preview_list.setViewMode(QtWidgets.QListView.IconMode)
        self.preview_list.setIconSize(QtCore.QSize(180,180))
        self.preview_list.setMinimumSize(QtCore.QSize(600,700)) # prevent changing size
        self.preview_list.setSpacing(10)
        # self.preview_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # info widgets
        self.pic_info = QtWidgets.QLabel()
        # pixmap = QtGui.QPixmap()
        # pixmap.load("C:\\Users\\spike\\Documents\\GitHub\\assetHelper\\image\\shose.0.png")
        # self.pic_info.setPixmap(pixmap)
        self.pic_info.setAlignment(QtCore.Qt.AlignCenter)
        self.pic_info.setMinimumSize(QtCore.QSize(395,500))

        self.text_info = QtWidgets.QLabel()
        self.text_info.setAlignment(QtCore.Qt.AlignHCenter )
        # self.text_info.setText(f"Asset Name: Shose\nPolycount: 30000\nDate Modified: 02/22/2025 12:22")
        custom_font = QtGui.QFont("Arial", 11)
        custom_font.setWeight(20);
        self.text_info.setFont(custom_font)
        self.text_info.setMinimumSize(QtCore.QSize(395,0))

        # Buttom widgets
        self.import_btn = QtWidgets.QPushButton("Import to Current Scene")
        self.import_btn.setFixedSize(200,30)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setFixedSize(50,30)

    # Create UI layouts and add widgets to respective layout
    def create_layouts(self):
        # Top buttons layout
        tool_bar_layout = QtWidgets.QHBoxLayout()
        tool_bar_layout.addWidget(self.load_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.remove_assets_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.info_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.setting_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addWidget(self.reset_btn, alignment=QtCore.Qt.AlignLeft)
        tool_bar_layout.addStretch()

        # info layout
        self.info_layout = QtWidgets.QVBoxLayout()
        self.info_layout.addWidget(self.pic_info)
        self.info_layout.addWidget(self.text_info)

        # preview layout
        self.center_layout = QtWidgets.QHBoxLayout()
        self.center_layout.addWidget(self.preview_list)
        # self.center_layout.addLayout(self.info_layout)

        # Buttom buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.close_btn)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(tool_bar_layout)
        # main_layout.addWidget(self.preview_list)
        main_layout.addLayout(self.center_layout)
        main_layout.addLayout(button_layout)

    # Create connection between UI and function
    def create_connections(self):
        self.load_assets_btn.clicked.connect(self.open_import_dialog)
        self.remove_assets_btn.clicked.connect(self.remove_selected_item)
        self.info_btn.clicked.connect(self.open_info_dialog)
        self.setting_btn.clicked.connect(self.open_setting_dialog)
        self.reset_btn.clicked.connect(self.reset_data)
        self.import_btn.clicked.connect(self.import_to_scene)
        self.preview_list.clicked.connect(self.highlight_item)
        self.close_btn.clicked.connect(self.close_windows) # test function

    # Functions for UI behavior
    def open_import_dialog(self, *arg):
        # check asset_dir in json
        if os.path.exists(self.JSON_PATH):
            if os.stat(self.JSON_PATH).st_size != 0:
                with open(self.JSON_PATH, "r") as file:
                 json_data = json.load(file)

        # if asset dir exist replace it else add to json
        if len(json_data) != 0 and list(json_data[0].keys())[0] == "asset_dir":
            self.ASSET_DIR = json_data[0]["asset_dir"]

        selected_file_paths = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", self.ASSET_DIR, self.FILE_FILTERS, self.selected_filter)[0]

        # If cancel clicked
        if not selected_file_paths: 
            print("Cancel Select File Window")
            return

        # Get all asset name in asset_list
        asset_list = [] #list for all asset name
        path_list = [] #list for all path
        for file in selected_file_paths:
            if self.check_not_in_list((os.path.splitext(os.path.basename(file))[0])):
                asset_list.append((os.path.splitext(os.path.basename(file))[0]))
                path_list.append(file)

        # If both list are not empty load the files and add to listview
        if len(asset_list) > 0 and len(path_list) > 0:
            # load files from path list
            for n in range (len(path_list)):
                helperFunctions.load_files(asset_list[n], path_list[n], self.JSON_PATH, self.IMAGE_DIR)

            # Add file name to preview
            self.asset_to_list(asset_list)
        else:
            print("All selected assets are in Assset Helper already")


    def remove_selected_item(self):
        helperFunctions.delete_load_asset(self.model.itemFromIndex(self.hilight_index).text(), self.JSON_PATH, self.IMAGE_DIR)
        self.model.removeRow(self.hilight_index.row())


    def open_info_dialog(self):
        if self.info_switch:
            self.info_layout.setParent(None)
            self.setMinimumWidth(700)
            self.setMaximumWidth(700)
            self.info_switch = False
        else:
            self.center_layout.addLayout(self.info_layout)
            self.setMinimumWidth(1100)
            self.setMaximumWidth(1100)
            self.info_switch = True



    def open_setting_dialog(self):
        setting_dialog = settingDialog.SettingDialog(self)
        setting_dialog.setObjectName("SettingWindow")
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
        color = QtGui.QColor(100, 100, 100, 127)
        brush = QtGui.QBrush(color)
        for asset_name in asset_list:
            item = QtGui.QStandardItem(asset_name) # set item name
            font = QtGui.QFont("Arial", 15) # create item font
            item.setFont(font) # set font
            item.setIcon(QtGui.QIcon(self.IMAGE_DIR + asset_name + ".0.png")) # set image icon
            item.setEditable(False) # set not editable
            item.setCheckable(True) # not use checkable for selection for now
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(brush)
            self.model.appendRow(item) # add to listview


    # Check if asset name is not in the listview 
    def check_not_in_list(self, asset_name):
        result = True
        for i in range (self.model.rowCount()):
            if asset_name == self.model.item(i).text():
                result = False
                break

        return result


    def highlight_item(self, index):
        # set class variable input item index
        self.hilight_index = index

        # 
        asset_name = self.model.itemFromIndex(index).text() # get asset name from clicked list item
        data_list = helperFunctions.get_asset_data(asset_name, self.JSON_PATH) # use asset name from json data

        # display geo snap shot
        pixmap = QtGui.QPixmap()
        pixmap.load(self.IMAGE_DIR + asset_name + ".0.png")
        self.pic_info.setPixmap(pixmap)

        # display geo info
        geo_info = f"Asset Name: {asset_name}\nPolycount: {data_list[0]}\nDate Modified: {data_list[2]}" # store display message
        self.text_info.setText(geo_info)


    def reset_data(self):
        message_dialog = QtWidgets.QMessageBox.question(self, "Reset all records", "Do you want to reset all the asset and setting?")
        if message_dialog == QtWidgets.QMessageBox.StandardButton.Yes:
            json_data = [] # create empty list to replace json data
            if os.path.exists(self.JSON_PATH):
                with open(self.JSON_PATH, "w") as file:
                    # dump empty data to json file
                    json.dump(json_data, file, indent=4)

            self.model.clear() # clear list view

            # delete all images
            images = os.listdir(self.IMAGE_DIR)
            for image in images:
                os.remove(self.IMAGE_DIR + image)


    # initialize data when asset helper window created
    def initialize_data(self):
        asset_list = [] # list for reading in existing json data
        if os.path.exists(self.JSON_PATH):
            if os.stat(self.JSON_PATH).st_size != 0:
                with open(self.JSON_PATH, "r") as file:
                    json_data = json.load(file)

                # append json data to empty list if it's asset data
                for data in json_data:
                    if list(data.keys())[0] != "asset_dir":
                        asset_list.append(list(data.keys())[0])
            self.asset_to_list(asset_list)


    def close_windows(self):
        children = self.children()
        if children[-1].objectName() == "SettingWindow":
            children[-1].destroy()
        self.close()

    # test function
    def test_print(self):
        self.load_assets_btn.resize(QtCore.QSize(113, 41))






if __name__ == "__main__":
    try:
        asset_helper_dialog.close() # pylint: disable=E0601
        asset_helper_dialog.deleteLater()
    except:
        pass

    asset_helper_dialog = AssetHelperDialog()
    asset_helper_dialog.show()