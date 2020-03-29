
class InputData:

    def __init__(self):

        # Folder name where .fbx files will be saved
        self.folderName = r'\fbx_files'

        # start name of object that we want to convert to .fbx file
        self.objName = 'Building'

        # database credentials
        self.hostName = 'localhost'
        self.databaseName = 'geotest2'
        self.userName = 'postgres'
        self.passwordSec = 'password123'
        # self.tableName = 'osm_test2' # polygon
        self.tableName = 'osm_test' # multipolygon