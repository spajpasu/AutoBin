import os
os.chdir(r'D:\UniDuE\hiwi\AutoBin\Project_Files\01_Blender\buildingCoordinate')

# importing blender path into system path
import sys
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

from importlib import reload

import Directory
reload(Directory)

a = Directory.Directory()
a.create_directory()
a.get_folder_path()
