# AssetHelper self UI
import maya.cmds as cmds
import importlib
import os

MENU_NAME = "AssetHelper"
ICON_PATH  = os.path.dirname(os.path.abspath(__file__)) + "\\icon\\"


def custom_shelf():
    delete_custom_shelf()

    cmds.shelfLayout(MENU_NAME, parent="ShelfLayout")

    cmds.shelfButton(parent=MENU_NAME, 
                     annotation='Asset Helper',
                     image1=ICON_PATH + "assetHelper_icon.png",
                     label='assetHelper',
                     command='import assetHelper;importlib.reload(assetHelper);assetHelper.assetHelper.AssetHelperDialog().show()')


def delete_custom_shelf():
    if cmds.shelfLayout(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME)