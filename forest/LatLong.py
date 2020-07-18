from importlib import reload
import InputData
import GeneralOperations as GO
from Database import Database
import GetCentorid

reload(InputData)

class LatLong:
    node_loc = {}
    forest_way = []
    wayIDS = []
    forest_relation = []
    forest_relation_ids = []
    closedWay_lat_lon = []

    buildingID = []
    buildingName = []
    buildingCoor = []

    # canal latitude longitude reader, stores the latitude and longitude location of canal in ways
    canal_lat_lon = []

    def __init__(self):
        self.node_loc = GO.read_nodes()
        # print(self.node_loc)
        self.wayIDS, self.forest_way = GO.forest_from_WAYS()
        self.forest_relation_ids, self.forest_relation = GO.data_from_RELATIONS(InputData.relationForest)
        self.closedWay_lat_lon = GO.lon_lat_from_way(self.node_loc, InputData.closedWAYS)

        self.buildingID, self.buildingName, self.buildingCoor = \
            GO.building_lon_lat(self.node_loc, InputData.buidlingDATA)

        # print(self.buildingCoor)

        # canal latitude longitude reader
        self.canal_lat_lon = GO.lon_lat_from_way(self.node_loc, InputData.canalData)
        # print(self.canal_lat_lon[0])

                
# for trees from ways directly run this method, node reference contains the node reference values as input(we get directly from osm)
    def get_wayID_nodeRef(self, Id, nodeRef):
        counter = 0
        lon_lat = []
        for i in nodeRef:
            iterable = GO.iterable_check(i)
            if iterable == False:
                j = str(i)
                pos = GO.get_lat_long(self.node_loc, int(j))
                GO.add_lat_long(pos, lon_lat)
            else:
                dummy_lon_lat = []
                if len(lon_lat) == 0:
                    lon_lat = [0] * len(nodeRef)
                    for k in i:
                        pos = GO.get_lat_long(self.node_loc, k)
                        GO.add_lat_long(pos, dummy_lon_lat)
                    lon_lat[counter] = dummy_lon_lat
                    counter = counter + 1
                else:
                    for k in i:
                        pos = GO.get_lat_long(self.node_loc, k)
                        GO.add_lat_long(pos, dummy_lon_lat)
                    lon_lat[counter] = dummy_lon_lat
                    counter = counter + 1
        # print(lon_lat)
        self.treeNode(Id, lon_lat)

# for trees from relations run this method, members contain way reference and type as key value pairs
    def read_latlon_ways(self, referenceId,  members):
        counter = 0
        values = []
        relationNodes = [0] * len(members)
        datafile = GO.open_file(InputData.wayDATA)
        for key, val in members.items():
            values.append(val)
            for line in datafile:
                if str(key) in line:
                    wayNodes = line.split('-')[1]
                    wayNodes = list(eval(wayNodes))
                    # relationNodes[counter] = wayNodes
                    if len(values) == 1:
                        relationNodes[counter] = wayNodes
                    else:
                        if values[0] != val:
                            relationNodes[counter] = wayNodes
                        else:
                            relationNodes[0].extend(wayNodes)
            counter = counter + 1
        try:
            relationNodes = list(filter(lambda x : x != 0, relationNodes))
        except Exception:
            print("No zero value \n")
        # relationNodes = list(filter(lambda x: x != 0, relationNodes))
        if len(relationNodes) == 1:
            relationNodes = relationNodes[0]
        # print(relationNodes, "\n")
        self.get_wayID_nodeRef(referenceId, relationNodes)

    def building_creator(self):
        connection, cursor = Database().connectDB()
        Database().createIndex(cursor)
        # minVecTot = []
        for i in range(0, len(self.buildingID)):
            minVector = GO.getPointMinLat(self.buildingCoor[i])
            GO.write_building_data(cursor, self.buildingID[i], self.buildingName[i], \
                self.buildingCoor[i], minVector)
        Database().dropIndex(cursor)
        Database().disconnectDB(connection, cursor)
        
            
    def treeNode(self, wayId, lon_lat):
        length = 0
        # print(len(lon_lat[0]))
        if len(lon_lat[0]) == 2:
            p = GO.create_Polygon(lon_lat)
            length = len(lon_lat)
        else:
            # print(lon_lat[0])
            p = GO.create_Polygon_with_hole(lon_lat[0], lon_lat[1::])
            for i in lon_lat:
                length = length + len(i)
        tree_loc = []
        for i in range(1, InputData.tree_density * length):
            point_in_poly = GO.get_random_point_in_polygon(p)
            if len(tree_loc) == 0:
                # print(point_in_poly)
                tree_loc.append(point_in_poly)
            else:
                val = GO.check_distance(point_in_poly, tree_loc)
                closed_way_check = GO.multi_polygon_point_check(self.closedWay_lat_lon, point_in_poly)
                if val >= InputData.distance_between_trees and closed_way_check:
                    tree_loc.append(point_in_poly)

        # print(len(tree_loc))
        GO.write_data(wayId, tree_loc)


    def canal_tree_creator(self):
        updatedLatLonTotal = []
        preciseLatLon = []
        for canalData in self.canal_lat_lon:
            updatedLatLonLocal = []
            polyObj = GO.create_Polygon(canalData)
            centroidOth = GetCentorid.polylabel(polyObj, tolerance=0.000001)
            for i in canalData:
                pointLoc = GO.canal_exterior_check(centroidOth.x, i[0])
                if pointLoc == 'r':
                    newPoint = GO.canal_exterior_changer(i, InputData.latAlter, -InputData.lonAlter)
                    updatedLatLonLocal.append(newPoint)
                else:
                    newPoint = GO.canal_exterior_changer(i, InputData.latAlter, InputData.lonAlter)
                    updatedLatLonLocal.append(newPoint)
            updatedLatLonTotal.append(updatedLatLonLocal)

        # create trees between updated canal data
        for i in updatedLatLonTotal:
            preciseLatLon.append(GO.canal_tree_generator(i))
        
        GO.write_text_file(preciseLatLon, InputData.canalTreeData)
        print("Points around canal created and can be accessed from {}".format(InputData.canalTreeData))
        # print(preciseLatLon)

    # def lat_Lon_Blender_Origin(self, osmID):
    #     # print(self.node_loc)
    #     lowestLatLon = GO.lowest_lat_lon_with_OSM(self.node_loc, InputData.buidlingDATA, osmID)
    #     print(lowestLatLon)