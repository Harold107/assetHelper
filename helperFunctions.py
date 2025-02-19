import json
import os
import datetime

import maya.cmds as cmds
import maya.api.OpenMaya as om2


def load_files(asset_name, file_path, json_path, image_dir):
    # Get vertex count
    object = cmds.file(file_path, i=True, ignoreVersion=True, returnNewNodes=True)
    vtx_count = 0
    for node in object:
        if cmds.nodeType(node) == "transform":
            cmds.select(node)
            vtx_count += get_vertices_count()

    # write to json
    modified_time = get_current_time()
    write_asset_info(asset_name, vtx_count, file_path, modified_time, json_path)

    # Clean up imported geo
    del_nodes = [] #list of all the transform nodes
    for node in object:
        if cmds.nodeType(node) == "transform":
            del_nodes.append(node)

    # group all objects from import
    cmds.select(del_nodes)
    selected_objs = cmds.ls(selection=True)
    if selected_objs:
        group_name = cmds.group(empty=True, name="asset_grp")
        cmds.parent(selected_objs, group_name)

    # save snap shot
    snap_shot(asset_name, group_name, image_dir)

    # Delete all in del_list
    cmds.delete(group_name)


# Get vertices list
def get_vertices_count(control_position = 0.0):
    sel = om2.MGlobal.getActiveSelectionList()
    node = sel.getComponent(0)[0]
    node_str_path_name = node.fullPathName()
    fn_mesh = om2.MFnMesh(node)
    points = fn_mesh.getPoints(space = 4)
    all_vertices = []
    for i in range(len(points)):
        all_vertices.append('{}.vtx[{}]'.format(node_str_path_name, i))

    return len(all_vertices)


# Write 
def write_asset_info(asset_name, vtx_count, asset_filepath, current_time, json_path):
    data = {asset_name:{"Polycount" : vtx_count, "Path" : asset_filepath, "Modified Date" : current_time}} #data dict for asset

    json_data = [] #data list to store asset dict

    # read in json data
    if os.path.exists(json_path):
        if os.stat(json_path).st_size != 0:
            with open(json_path, "r") as file:
                json_data = json.load(file)

    # Add asset data if it's not already existed
    if check_asset_exist(asset_name, json_data):
        print(f"{asset_name} is already in library")
    else:
        # write new data to json
        with open(json_path, "w") as file:
            json_data.append(data)
            json.dump(json_data, file, indent=4)


# Remove asset data from json and image preview
def delete_load_asset(asset_name, json_path, image_dir):
    if os.path.exists(json_path):
        if os.stat(json_path).st_size != 0:
            with open(json_path, "r") as file:
                json_data = json.load(file)

    # remove item from list if name is the key
    for n in range (len(json_data)):
        if asset_name in json_data[n]:
            json_data.pop(n)
            break
        elif n == len(json_data):
            print(f"{asset_name} is not in the json data")

    # remove associated image file
    os.remove(image_dir + f"{asset_name}.0.png")

    with open(json_path, "w") as file:
        json.dump(json_data, file, indent=4)


# Check is asset data in json
def check_asset_exist(asset_name, json_data):
    for n in range (len(json_data)):
        if asset_name in json_data[n]:
            return True
    return False


# Get current system time
def get_current_time():
    # Get year, month, dat, hour, minute
    current_time = datetime.datetime.now()
    ct_year = current_time.year
    ct_month = str(current_time.month)
    ct_day = current_time.day
    ct_hour = current_time.hour
    ct_minute = str(current_time.minute)

    # Padding 0 for month and minute if it's 1 digit
    if len(ct_month) < 2:
        ct_month = "0" + ct_month
    if len(ct_minute) < 2:
        ct_minute = "0" + ct_minute

    return (f"{ct_month}/{ct_day}/{ct_year}  {ct_hour}:{ct_minute}")


# Get asset daya
def get_asset_data(asset_name, json_path):
    data_list = []
    if os.path.exists(json_path):
        if os.stat(json_path).st_size != 0:
            with open(json_path, "r") as file:
                json_data = json.load(file)

        for data in json_data:
            if asset_name in data:
                data_list.append(data[asset_name]["Polycount"])
                data_list.append(data[asset_name]["Path"])
                data_list.append(data[asset_name]["Modified Date"]) 
                break
        return data_list


def snap_shot(asset_name, group_name, image_dir):
    cameraName = cmds.camera(name="snap_cam", 
                             position=(5,5,5),
                             focalLength=75 )

    # Render assets
    cmds.currentUnit(linear="meter")

    # Select group to frame within camera
    cmds.select(group_name)

    # set Perspective camera position
    cmds.xform(cameraName[0], ws=True, translation=(-3.885, 4.732, 12.531))
    cmds.xform(cameraName[0], ws=True, rotation=(-14.4, -23.6, 0.0))
    # Set camera focal length to 85
    cmds.setAttr(cameraName[1] + ".focalLength", 85)
    cmds.viewFit(cameraName[1])  # Frame camera view to fit object scale
    cmds.lookThru(cameraName[0])
    cmds.currentUnit(linear="cm")
    cmds.select(clear=True)
    cmds.playblast(filename = image_dir + asset_name,
                    frame=[1],
                    percent=100,
                    framePadding=0,
                    compression="png",
                    viewer=False,
                    clearCache=True,
                    format="image",
                    widthHeight=(300,300),
                    showOrnaments = False)
    cmds.delete(cameraName[0])

# Testing
# load_files("two_set", "C:\\Users\\spike\\Desktop\\New Folder\\two_set.ma", "C:/Users/spike/Documents/GitHub/assetHelper/assetinfo.json")

# snap_shot("pTorus1", "C:\\Users\\spike\\Documents\\GitHub\\assetHelper\\image\\")