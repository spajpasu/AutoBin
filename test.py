import Forest
import LatLong
import InputData

'''osmium is developed with concept of handler, which takes in file name, it has some predefined functions that we can 
use to get the data from OSM file'''

# number of trees corresponding to each node

h = Forest.ForestDataHandler()

# print(InputData.path)
# location of file goes as input to apply_file
h.apply_file(InputData.path)

# LatLong.LatLong().plot_nodes()