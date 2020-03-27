# import Dimensions
# changing the current working directory
import os
os.chdir(r'D:\UniDuE\hiwi\AutoBin\Project_Files\01_Blender\buildingCoordinate')

# importing blender path into system path
import sys
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

from importlib import reload
import FbxFiles
reload(FbxFiles)

a = FbxFiles.FbxFiles()
a.changeSettings()

for obj in bpy.data.objects:
    objectName = a.checkObjType(obj)
    if objectName != 0:
        a.fileCreation(obj)
    else:
        continue
a.revertSettings()
print('.fbx files of all %s completed.' % a._obj_Name)

