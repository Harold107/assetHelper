import json
import os
import datetime

import maya.cmds as cmds
import maya.api.OpenMaya as om2


def load_files(asset_name, file_path, json_path):
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

    # Delete all in del_list
    for node in del_nodes:
        cmds.select(node)
        cmds.delete()


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


# Remove asset data from json
def delete_load_asset(asset_name, json_path):
    if os.path.exists(json_path):
        if os.stat(json_path).st_size != 0:
            with open(json_path, "r") as file:
                json_data = json.load(file)

    for n in range (len(json_data)):
        if asset_name in json_data[n]:
            json_data.pop(n)
            break
        elif n == len(json_data):
            print(f"{asset_name} is not in the json data")



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



# Testing
# delete_load_asset("sphere", "C:/Users/spike/Documents/GitHub/assetHelper/assetinfo.json")

