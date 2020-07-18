import LatLong
import InputData
import GeneralOperations as GO

a = LatLong.LatLong()

a.canal_tree_creator()

# osmID = input("Enter the osm ID of building whose lowest latitude and longitude needs to be found: \n")

# a.lat_Lon_Blender_Origin(osmID)

# delete canal data file after trees are generated


GO.remove_files(InputData.wayDATA)
GO.remove_files(InputData.forestinWAYS)
GO.remove_files(InputData.closedWAYS)
GO.remove_files(InputData.relationForest)
GO.remove_files(InputData.buidlingDATA)
GO.remove_files(InputData.canalData)

GO.remove_files(InputData.nodeDATA)