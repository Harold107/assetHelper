import maya.cmds as cmds
import maya.api.OpenMaya as om2


file_path = r"C:\Users\Aro\Desktop\New folder\cube.ma"

def load_files(file_path):
    object = cmds.file(file_path, i=True, ignoreVersion=True, returnNewNodes=True)
    cmds.select(object)
    # print(object)
    for node in object:
        if cmds.nodeType(node) == "transform":
            


def get_asset_info():
    sel = om2.MGlobal.getActiveSelectionList()
    node = sel.getComponent(0)[0]
    node_str_path_name = node.fullPathName()
    fn_mesh = om2.MFnMesh(node)
    points = fn_mesh.getPoints(space = 4)
    all_vertices = []
    for i in range(len(points)):
        all_vertices.append('{}.vtx[{}]'.format(node_str_path_name, i))
    return all_vertices


def write_asset_info():
    pass


def delete_load_asset():
    pass



load_files(file_path)