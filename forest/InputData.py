path = "/home/ajaykumar/work/AutoBin/Project_Files/osm2postgres/sampleDortmund.osm"

# % tree data
tree_density = 1
distance_between_trees = 0.01

trees_bn_nodes = 3

# the input arguments to change positions of latitude and longitude of trees around canal
latAlter = 0.00001
lonAlter = 0.00015


# # Dictionary to extract required way information
# requiredWAYS = {"landuse": ['railway', 'forest'] }

# File name data
wayDATA = 'wayDATA.txt'
forestinWAYS = 'forest.txt'
closedWAYS = 'closedWay.txt'
relationForest = 'relationForest.txt'
nodeDATA = 'nodeDATA.txt'
buidlingDATA = 'building.txt'

# file to write canal data to generate trees
canalData = 'canalData.txt'
canalTreeData = 'C-TressData.txt'

requiredTags = 'required-tags.txt'


# Database credentials
hostName = 'localhost'
databaseName = 'geotest2'
userName = 'usertest'
passwordSec = 'password'
# self.tableName = 'osm_test2' # polygon
tableName = 'osm_test2'  # multipolygon
