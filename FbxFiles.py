from importlib import reload

import InputData
import Directory
reload(InputData)
reload(Directory)
from InputData import InputData
from Directory import Directory

import bpy

class FbxFiles:

    _obj_Name = 'Building'

    def __init__(self, objName = InputData().objName):

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
        Directory().create_directory()
        folder = Directory().get_folder_path()
        FbxFiles().deselectAllObj()
        object.select_set(True)
        path = folder + r'\\' + object.name + '.fbx'
                                                                    # check these two
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True, use_custom_props=True,
                                 axis_forward='-Z', axis_up='Y')

    def deselectAllObj(self):
        bpy.ops.object.select_all(action='DESELECT')


    def revertSettings(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        FbxFiles().deselectAllObj()

    # check if cell in DB is already full and ask for conformation if yes
    def cellCheck(self):

        pass

    # should save the file location into postGIS database
    def save_filename_postGIS(self, path):

        pass

