import json

import maya.cmds as cmds
import maya.api.OpenMaya as om2


file_path = r"C:\Users\Aro\Desktop\New folder\cube.ma"

def load_files(file_path):
    object = cmds.file(file_path, i=True, ignoreVersion=True, returnNewNodes=True)

    for node in object:
        if cmds.nodeType(node) == "transform":
            cmds.select(node)
            vtx_count = get_vertices_count()

    # write to json
    asset_name = "Cube"
    asset_filepath = "Place Holder"
    json_path = "C:/Users/Aro/Documents/GitHub/assetHelper/assetinfo.json"
    write_asset_info(asset_name, vtx_count, asset_filepath, json_path)

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


def write_asset_info(asset_name, vtx_count, asset_filepath, json_path):
    # print("PolyCount: " + str(vtx_count))

    obj_name = cmds.ls(sl=True)

    # data = {str(obj_name[0]):{"Polycount" : vtx_count, "Path" : asset_filepath}}
    data = {asset_name:{"Polycount" : vtx_count, "Path" : asset_filepath}}

    json_data = []
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


def delete_load_asset(asset_name, json_path):
    if os.path.exists(json_path):
        if os.stat(json_path).st_size != 0:
            with open(json_path, "r") as file:
                json_data = json.load(file)

    for n in range (len(json_data)):
        if asset_name in json_data[n]:
            json_data.pop(n)
        else:
            print(f"Didn't find asset called {asset_name}")

    with open(json_path, "w") as file:
        json.dump(json_data, file, indent=4)
    # print(json_data)


def check_asset_exist(asset_name, json_data):
    for n in range (len(json_data)):
        if asset_name in json_data[n]:
            return True
        else:
            return False


# cmds.file(f=True, newFile=True)
# load_files(file_path)
delete_load_asset("cube", "C:/Users/Aro/Documents/GitHub/assetHelper/assetinfo.json")