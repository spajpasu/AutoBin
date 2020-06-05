from importlib import reload
from shapely.geometry import Polygon, Point, LineString
from shapely import wkb
from Database import Database
import random
import InputData

reload(InputData)

def read_nodes():
    n = {}
    data = open_file(InputData.nodeDATA)
    for line in data:
        a = str.split(line, ':')
        n[int(a[0])] = list(eval(a[1]))
    return n


def iterable_check(object):
    try:
        iter(object)
    except Exception:
        return False
    else:
        return True

def lon_lat_from_way(nodeDATA, filename):
    railwayDATA = []
    data = open_file(filename)
    for line in data:
        lon_lat = []
        a = list(eval(str.split(line, '-')[1]))
        for i in a:
            lon_lat.append(get_lat_long(nodeDATA, i))
        railwayDATA.append(lon_lat)
    # print(railwayDATA)
    return railwayDATA

def forest_from_WAYS():
    wayIDS = []
    forestWayDATA = []
    data = open_file(InputData.forestinWAYS)
    for line in data:
        wayID = str.split(line, '-')[0]
        references = list(eval(str.split(line, '-')[1]))
        wayIDS.append(wayID)
        forestWayDATA.append(references)
    return wayIDS, forestWayDATA

def data_from_RELATIONS(filename):
    relationIDS = []
    forestRelationDATA = []
    data = open_file(filename)
    for line in data:
        a = str.split(line, '-')
        relationID = a[0]
        relationMembers = a[1]
        relatioRefTyp = {}
        memberDivide = str.split(relationMembers, ',')
        for i in memberDivide:
            divideA = str.split(i, ':')
            if len(divideA) >= 2:
                relatioRefTyp[int(divideA[0])] = divideA[1]
        forestRelationDATA.append(relatioRefTyp)
        relationIDS.append(relationID)
    return relationIDS, forestRelationDATA

def get_nodeID_loc(nodes, nodeID, location):
    nodes[nodeID] = location
    # print(nodes)
    return nodes

def get_lat_long(nodes, id):
    return nodes.get(id)

# def create_railway_data(railway, )

def add_lat_long(pos, lon_lat):
    # position = str(pos)
    # a = position.split('/')
    # a = [float(a[0]), float(a[1])]
    lon_lat.append(pos)

def check_distance(point, tree_nodes):
    return_length = 1
    for i in tree_nodes:
        line = LineString([i, point])
        if line.length < return_length:
            return_length = line.length
    return return_length

def get_random_point_in_polygon(poly):
    minx, miny, maxx, maxy = poly.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p):
            # print(p)
            return p

def create_Polygon(lon_lat):
    poly = Polygon(lon_lat)
    return poly

def create_Polygon_with_hole(exterior, interior):
    poly = Polygon(shell=exterior, holes=interior)
    return poly

def point_check_polygon(polygon, point):
    if polygon.contains(point):
        return True
    else:
        return False

def multi_polygon_point_check(railway_nodes, point):
    decision = True
    for i in railway_nodes:
        poly = create_Polygon(i)
        newdecision = point_check_polygon(poly, point)
        if newdecision:
            return not(newdecision)
    return decision

def write_data(wayID, tree_loc):
    connection, cursor = Database().connectDB()
    j = ''
    for i, tree_point in enumerate(tree_loc):
        val_check = Database().id_check_execute(cursor, str(wayID)+str(i))
        if val_check:
            if j == 'yes':
                query = "INSERT INTO {} (osm_id, obj_type, osm_point) VALUES({}, {}, {});"\
                    .format(InputData.tableName, str(wayID)+str(i), "'Tree'", point_to_string(tree_point))
                print(query)
                Database().insertDATA(cursor, query)
            else:
                res = Database().decisionCheck(str(wayID)+str(i))
                if res == 'y' or res == 'yes':
                    query = "INSERT INTO {} (osm_id, obj_type, osm_point) VALUES({}, {}, {});"\
                        .format(InputData.tableName, str(wayID)+str(i), "'Tree'", point_to_string(tree_point))
                    print(query)
                    Database().insertDATA(cursor, query)
                    j = res
                else:
                    print('The value in DataBase has not changed.')

        else:
            query = "INSERT INTO {} (osm_id, obj_type, osm_point) VALUES({}, {}, {});"\
                .format(InputData.tableName, str(wayID)+str(i), "'Tree'", point_to_string(tree_point))
            print(query)
            Database().insertDATA(cursor, query)
    Database().disconnectDB(connection, cursor)

# def write_data(wayID, tree_loc):
#     if iterable_check(tree_loc[0]):
#         for i in tree_loc:
#             for j in i:
#                 print(j.wkb_hex)
#     else:
#         for i in tree_loc:
#             print(i.wkb_hex)

# start writing data to database

def open_file(filename):
    f = open(filename, 'r') # move this to a function in General Operations
    datafile = f.readlines()
    f.close()
    return datafile

def create_tagValKey(fileHandler):
    finList = []
    newList = [line.rstrip() for line in fileHandler]
    # print(newList)
    for i in newList:
        a = i.split('=')
        finList.append(a)
    return finList

def point_to_string(point):
    return "'" + str(point) + "'"