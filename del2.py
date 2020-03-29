# import FbxFiles
# import Directory

# a = FbxFiles.FbxFiles()
# a.checkObjType('Building')
# Directory.Directory().create_directory()
# b = Directory.Directory().get_folder_path()
# print(b)
# id = "'543.265.188'"
# name = "'Building_1234'"
# point = "'POINT(3 7)'"
# polygon = "'PLOYGON((1 2, 6 1, 9 3, 7 5, 3 6, 1 2))'"
# path = "'D:\\UniDuE\\hiwi\\AutoBin\\Project_Files\\01_Blender\\osm2postgre\\Dortmund_small_test.osm'"
#
# print("INSERT INTO %s(osm_id, osm_name, osm_polygon, osm_point, file_path) VALUES(%s, %s, %s, %s, %s)" %('name', id, name, point, polygon, path))
# a = 'Building_53815668'
# b = a.split('_')
# print(b)
# c = int(b[1])
# print(c)
# import os.path
#
#
# def createFile():
#     fileName = 'yes'+'.txt'
#     if os.path.exists(fileName):
#         print('File with name %s exists.' % fileName)
#         decision = input('Do you want to delete file? y/n : ')
#         if decision == 'y':
#             os.remove(fileName)
#         else:
#             fileName = input('Enter name of file to create: ') + '.txt'
#             open(fileName, 'w+')
#     else:
#         print("File with %s name created." %fileName)
#         open(fileName, 'w+')
#
# createFile()

a = 2
b = 888888888888888
print('vale of a is {}, {}'.format(a, b))