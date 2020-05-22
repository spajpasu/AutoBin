import random
from shapely.geometry import Polygon, Point, LineString
import InputData
import re

class LatLong:
    f = open('wayDATA.txt', 'r')
    datafile = f.readlines()
    f.close()
    _node_loc = {}

    def get_nodeID_loc(self, nodeID, location):
        self._node_loc[nodeID] = location

    def get_wayID_nodeRef(self, wayID, nodeRef):
        lon_lat = []
        # print(str(wayID) + ' ' + str(nodeRef))
        for i in nodeRef:
            j = str(i)
            pos = self.get_lat_long(int(j))
            self.add_lat_long(pos, lon_lat)
        lon_lat_float = self.change_type(lon_lat)
        # print(lon_lat_float)
        self.treeNode(lon_lat_float)

    def get_relationID_nodeRef(self, relationID, nodeRef):
        # lon_lat = [0] * len(nodeRef)
        # for i in nodeRef:
        pass
        #     print(len(i))
        #     j = str(i)
        #     pos = self.get_lat_long(int(j))
        #     self.add_lat_long(pos, lon_lat)
        # lon_lat_float = self.change_type(lon_lat)
        # # print(lon_lat_float)
        # self.treeNode(lon_lat_float)

    def read_latlon_ways(self, relationID, members):
        counter = 0
        values = []
        wayNodes = []
        relationNodes = [0] * len(members)
        for key, val in members.items():
            values.append(val)
            for line in self.datafile:
                if key in line:
                    wayNodes = line.split('-')[1]
                    wayNodes = list(eval(wayNodes))
                    # relationNodes[counter] = wayNodes
                    if len(values) == 1:
                        relationNodes[counter] = wayNodes
                    else:
                        if values[0] != val:
                            relationNodes[counter] = wayNodes
                        else:
                            # relationNodes.remove(0)
                            # relationNodes = self.add_list_elements(relationNodes, wayNodes)
                            relationNodes[0].extend(wayNodes)
            counter = counter + 1
        # try:
        #     relationNodes = list(filter(lambda x : x != 0, relationNodes))
        # except Exception:
        #     print("No zero value \n")
        relationNodes = list(filter(lambda x: x != 0, relationNodes))
        print(relationNodes, "\n")
        self.get_relationID_nodeRef(relationID, relationNodes)

    def change_type(self, strList):
        returnVal = []
        for i in strList:
            returnVal.append([float(i[0]), float(i[1])])
        return returnVal

    def get_lat_long(self, id):
        return self._node_loc.get(id)

    def add_lat_long(self, pos, lon_lat):
        position = str(pos)
        a = position.split('/')
        lon_lat.append(a)

    def treeNode(self, lon_lat):
        p = Polygon(lon_lat)
        tree_loc = []
        for i in range(1, InputData.tree_density * len(lon_lat)):
            point_in_poly = self.get_random_point_in_polygon(p)
            # tree_loc.append(point_in_poly)
            if len(tree_loc) == 0:
                tree_loc.append(point_in_poly)
            else:
                val = self.check_distance(point_in_poly, tree_loc)
                if val >= InputData.distance_between_trees:
                    tree_loc.append(point_in_poly)
                    # check if location of tress coincide with other objects and finally write data into database
        self.print_data(tree_loc)

    def check_distance(self, point, tree_nodes):
        return_length = 1
        for i in tree_nodes:
            line = LineString([i, point])
            if line.length < return_length:
                return_length = line.length
        return return_length

    def print_data(self, tree_loc):
        for i in tree_loc:
            print("{0} {1}".format(i.x, i.y))

    def get_random_point_in_polygon(self, poly):
        minx, miny, maxx, maxy = poly.bounds
        while True:
            p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if poly.contains(p):
                return p

    def iterable_check(self, object):
        try:
            iter(object)
        except Exception:
            return False
        else:
            return True
