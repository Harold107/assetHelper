import maya.cmds as cmds
import maya.api.OpenMaya as om2
import json
import os

def get_poly_count(control_position = 0.0):
    sel = om2.MGlobal.getActiveSelectionList()
    node = sel.getComponent(0)[0]
    node_str_path_name = node.fullPathName()
    fn_mesh = om2.MFnMesh(node)
    points = fn_mesh.getPoints(space = 4)
    all_vertices = []
    for i in range(len(points)):
        all_vertices.append('{}.vtx[{}]'.format(node_str_path_name, i))
    return all_vertices

def write_geo_info():
    vertex_count = get_poly_count()
    print("PolyCount: " + str(len(vertex_count)))

    obj_name = cmds.ls(sl=True)
    asset_filepath = "place_holder"

    data = {str(obj_name[0]):{"Polycount" : len(vertex_count), "Path" : asset_filepath}}
    file_data = []
    file_path = "C:/Users/Aro/Documents/GitHub/assetHelper/assetinfo.json"
    if os.path.exists(file_path):
        if os.stat(file_path).st_size != 0:
            with open(file_path, "r") as file:
                file_data = json.load(file)         
    with open(file_path, "w") as file:
        file_data.append(data)
        json.dump(file_data, file, indent=4)

#write_geo_info()