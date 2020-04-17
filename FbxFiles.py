from importlib import reload

import InputData
import Directory
import math
reload(InputData)
reload(Directory)
# from InputData import InputData
# from Directory import Directory

import bpy

class FbxFiles:

    _obj_Name = ''

    def __init__(self, objName = InputData.InputData().objName):

        if len(objName) > 0: FbxFiles._obj_Name = objName

    def lowest_lat_long(self, object): # change this
        if object.type == 'MESH':
            n = len(object.data.vertices.data.vertices.values())
            length = [0] * n
            mat = object.matrix_world
            for i in range(0, n):
                length[i] = math.sqrt((object.data.vertices[i].co[0]) ** 2 + (object.data.vertices[i].co[1]) ** 2 + (object.data.vertices[i].co[2]) ** 2)
            # print(length)
            j = length.index(min(length))
            return mat @ object.data.vertices[j].co
        else:
            print("Model is not of type 'MESH'")
            return 1

    def set_origin_to_world(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        FbxFiles().deselectAllObj()


    def change_settings(self, point):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.cursor.location = point
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # this should return true if building
    def checkObjType(self, object):
        if (object.name).startswith(FbxFiles._obj_Name):
            return object.name
        else:
            return 0

    # create fbx file in the folder created with name of building and osm_id
    def fileCreation(self, object):
        FbxFiles().deselectAllObj()
        object.select_set(True)
        path = Directory.Directory().get_folder_path() + '\\' + object.name + '.fbx'
                                                                    # check these two
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True, use_custom_props=True,
                                 axis_forward='-Z', axis_up='Y')
        FbxFiles().revertSettings()
        return path

    def deselectAllObj(self):
        bpy.ops.object.select_all(action='DESELECT')


    def revertSettings(self): #Change this
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        FbxFiles().deselectAllObj()

    # get osm_id of object given in Input file
    def get_osm_id(self, object):
        osm_id = object.name.split('_')
        return int(osm_id[1])

