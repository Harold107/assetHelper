from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    # return maya main window for parenting
    main_window_ptr = omui.MQtUtil.mainWindow() #C++ window pointer to python object
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(300)
        self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False) #remove the ? on dialog

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox("Check Box 1")
        self.checkbox1 = QtWidgets.QCheckBox("Check Box 2")
        self.button1 = QtWidgets.QPushButton("Button 1")
        self.button2 = QtWidgets.QPushButton("Button 2")

    def create_layouts(self):
        pass

if __name__ == "__main__":
    #__name__ is __main__ when excute the code in script editor buffer
    d = TestDialog()
    d.show()