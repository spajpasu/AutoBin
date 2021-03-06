'''Python class which takes dictionary as input with Key as name of object and value as its location and checks if the
name of object is a building or not and '''
import os.path

from importlib import reload

import InputData
import FbxFiles
reload(InputData)
reload(FbxFiles)
# from InputData import InputData
# from FbxFiles import FbxFiles

class Directory:
    __folder_name   = ''

    def __init__(self, folderName = InputData.InputData().folderName):
        if len(folderName) > 0: Directory.__folder_name = folderName

    # creates a directory with name specified during class object creation, else creates a directory with default name
    def create_directory(self):
        try:
            if not os.path.exists(os.getcwd() + Directory.__folder_name):
                os.mkdir(os.getcwd() + Directory.__folder_name)
                print("Directory made")
        except OSError:
            print('Error Creating Directory' + os.getcwd() + Directory.__folder_name)

    # returns the path of the folder created to save .fbx files
    def get_folder_path(self):
        print('.fbx files saved in:\n %s'% os.getcwd() + Directory.__folder_name)
        return (os.getcwd() + Directory.__folder_name)

    def createFile(self):
        fileName = FbxFiles.FbxFiles()._obj_Name+'.txt'
        if os.path.exists(fileName):
            print('File with name %s exists and overwriting.' %fileName)
        else:
            open(fileName,'w+')
        return fileName



