# import Dimensions
# changing the current working directory
import os
os.chdir(r'D:\UniDuE\hiwi\AutoBin\Project_Files\01_Blender\buildingCoordinate')

# importing blender path into system path
import sys
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from importlib import reload
import FbxFiles
import Directory
reload(FbxFiles)
reload(Directory)

a = FbxFiles.FbxFiles()
b = Directory.Directory()
b.create_directory()
file = b.createFile()
a.set_origin_to_world()
f = open(file, 'w')

for obj in bpy.data.objects:
    objectName = a.checkObjType(obj)
    if objectName != 0:
        point = a.lowest_lat_long(obj)
        if point != 1:
            a.change_settings(point)
            path = a.fileCreation(obj)
            osm_id = a.get_osm_id(obj)
            f.write(str(osm_id) + '\t' + path + '\n')
        # f.write(osm_id)
    else:
        continue
f.close()

print('.fbx files of all %s completed.' % a._obj_Name)

