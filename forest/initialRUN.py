import LatLonCreator
import LatLong
import InputData
import GeneralOperations as GO

'''osmium is developed with concept of handler, which takes in file name, it has some predefined functions that we can 
use to get the data from OSM file'''

# number of trees corresponding to each node

# print(GO.node_loc)
# print(GO.railway_polygon)

h = LatLonCreator.ForestDataHandler()

# print(InputData.path)
# location of file goes as input to apply_file
h.apply_file(InputData.path)

print('Files Created')


# LatLong.LatLong().plot_nodes()