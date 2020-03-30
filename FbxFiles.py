from importlib import reload

import InputData
import Directory
reload(InputData)
reload(Directory)
# from InputData import InputData
# from Directory import Directory

import bpy

class FbxFiles:

    _obj_Name = ''

    def __init__(self, objName = InputData.InputData().objName):

        if len(objName) > 0: FbxFiles._obj_Name = objName

    def changeSettings(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

    # this should return true if building
    def checkObjType(self, object):
        if (object.name).startswith(FbxFiles._obj_Name):
            return object.name
        else:
            return 0
        # print(FbxFiles.__obj_Name)
        # p rint('Object with name %s does not exist'%FbxFiles.__obj_Name)
        # a = bpy.data.objects['Building_53815693'].name
        # print(a)

    # should save the values of original location
    # def originalLocation(self, object):
    #     return object.location

    # should change the coordinates of object to origin
    # def changeToOrigin(self):
    #     pass

    # create fbx file in the folder created with name of building and osm_id
    def fileCreation(self, object):
        FbxFiles().deselectAllObj()
        object.select_set(True)
        path = Directory.Directory().get_folder_path() + '\\' + object.name + '.fbx'
                                                                    # check these two
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True, use_custom_props=True,
                                 axis_forward='-Z', axis_up='Y')
        return path

    def deselectAllObj(self):
        bpy.ops.object.select_all(action='DESELECT')


    def revertSettings(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        FbxFiles().deselectAllObj()

    # get osm_id of object given in Input file
    def get_osm_id(self, object):
        osm_id = object.name.split('_')
        return int(osm_id[1])

