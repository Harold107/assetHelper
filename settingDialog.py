import sys

from PySide2 import QtCore
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
        # self.setMinimumWidth(200)
        # self.setMinimumHeight(200)
        # self.setMaximumWidth(200)
        # self.setMaximumHeight(200)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        pass

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)