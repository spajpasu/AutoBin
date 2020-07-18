from importlib import reload
from shapely.geometry import Polygon, Point, LineString
from Database import Database
import os
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

def building_lon_lat(nodeDATA, filename):
    buildingID = []
    buildingName = []
    buildingCoor = []
    data = open_file(filename)
    for line in data:
        lon_lat = []
        testString = str.split(line, '~')
        buildingID.append(eval(testString[0]))
        # print(buildingID)
        buildingName.append(testString[1])
        # print(buildingName)
        a = list(eval(testString[2]))
        for i in a:
            lon_lat.append(get_lat_long(nodeDATA, i))
        buildingCoor.append(lon_lat)
    # print(buildingCoor)
    # print(railwayDATA)
    return buildingID, buildingName, buildingCoor

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
    Database().createIndex(cursor)
    print("{} trees generated for ID {}.".format(len(tree_loc), wayID))
    databaseDecision = input("Do you want to write data to database yes/no ? \n")
    if databaseDecision == 'yes':
        j = ''
        for i, tree_point in enumerate(tree_loc):
            val_check = Database().id_check_execute(cursor, str(wayID)+str(i))
            if val_check:
                if j == 'yes':
                    query = "UPDATE {} SET osm_point = {} where osm_id = {};"\
                        .format(InputData.tableName, point_to_string(tree_point), str(wayID)+str(i))
                    print(query)
                    Database().insertDATA(cursor, query)
                else:
                    res = Database().decisionCheck(str(wayID)+str(i))
                    if res == 'y' or res == 'yes':
                        query = "UPDATE {} SET osm_point = {} where osm_id = {};"\
                        .format(InputData.tableName, point_to_string(tree_point), str(wayID)+str(i))
                        print(query)
                        Database().insertDATA(cursor, query)
                        j = res
                    else:
                        print('The value in DataBase has not changed.\n')

            else:
                query = "INSERT INTO {} (osm_id, obj_type, osm_point) VALUES({}, {}, {});"\
                    .format(InputData.tableName, str(wayID)+str(i), "'Tree'", point_to_string(tree_point))
                print(query)
                Database().insertDATA(cursor, query)
    else:
        print("No data has been written to database.\n")
    Database().dropIndex(cursor)
    Database().disconnectDB(connection, cursor)

def write_building_data(cursor, osm_id, osm_name, osm_polygon, osm_point):
    val_check = Database().id_check_execute(cursor, str(osm_id))
    if val_check:
        if osm_name == 'None':
            print('Record with osm_id - {} already exists and hence overwriting'.format(osm_id))
            query = "UPDATE {} SET osm_polygon = {}, osm_point = {} WHERE osm_id = {};"\
                .format(InputData.tableName, db_polygon_generator(osm_polygon),\
                    db_point_generator(osm_point), str(osm_id))
            print(query)
            Database().insertDATA(cursor, query)
        else:
            print('Record with osm_id - {} already exists and hence overwriting'.format(osm_id))
            query = "UPDATE {} SET osm_name = {}, osm_polygon = {}, osm_point = {} WHERE osm_id = {};"\
                .format(InputData.tableName, "'" + str(osm_name) + "'", db_polygon_generator(osm_polygon),\
                    db_point_generator(osm_point), str(osm_id))
            print(query)
            Database().insertDATA(cursor, query)
    else:
        if osm_name == 'None':
            query = "INSERT INTO {} (osm_id, osm_polygon, osm_point) VALUES({}, {}, {});"\
                .format(InputData.tableName, str(osm_id), \
                    db_polygon_generator(osm_polygon), db_point_generator(osm_point))
            print(query)
            Database().insertDATA(cursor, query)
        else:
            query = "INSERT INTO {} (osm_id, osm_name, osm_polygon, osm_point) VALUES({}, {}, {}, {});"\
                .format(InputData.tableName, str(osm_id), "'" + str(osm_name) + "'", \
                    db_polygon_generator(osm_polygon), db_point_generator(osm_point))
            print(query)
            Database().insertDATA(cursor, query)

# def write_data(wayID, tree_loc):
#     if iterable_check(tree_loc[0]):
#         for i in tree_loc:
#             for j in i:
#                 print(j.wkb_hex)
#     else:
#         for i in tree_loc:
#             print(i.wkb_hex)

# start writing data to database

def getPointMinLat(pointData):
    # print(pointData)
    if len(pointData) != 0:
        minVector = pointData[0]
        for i in range(1, len(pointData)):
            if pointData[i][0] < minVector[0]:
                minVector = pointData[i]
            elif(pointData[i][0] == minVector[0]):
                if pointData[i][1] < minVector[1]:
                    minVector = pointData[i]
        return minVector
    else:
        return None
                

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

def remove_files(fileName):
    os.remove(fileName)
    print("Removed text file {}".format(fileName))

def db_point_generator(point):
    return "'" + 'POINT(' + str(point[0]) + ' ' + str(point[1]) + ')' + "'"

def db_polygon_generator(points):
    length = len(points)
    returnVal = "'" + 'POLYGON((' 
    for i in range(0, length):
        returnVal = returnVal + str(points[i][0]) + ' ' + str(points[i][1])
        if i < length - 1:
            returnVal = returnVal + ','
    returnVal = returnVal + '))' + "'"
    return returnVal

def canal_exterior_check(centroidX, pointX):
    if centroidX - pointX > 0:
        return 'r'
    else:
        return 'l'

def canal_exterior_changer(originalLatLon, latChan, lonChan):
    # print(type(originalLatLon[0]))
    changeLatLon = [originalLatLon[0] + latChan, originalLatLon[1] + lonChan]
    return changeLatLon

def canal_tree_generator(polyOne):
    precisePoint = []
    for i in range(0, len(polyOne)-1):
        xDiv = (polyOne[i+1][0] - polyOne[i][0])/InputData.trees_bn_nodes
        yDiv = (polyOne[i+1][1] - polyOne[i][1])/InputData.trees_bn_nodes
        # print('{}, {}'.format(xDiv, yDiv))
        precisePoint.append(polyOne[i])
        for j in range(1, InputData.trees_bn_nodes):
            a = [polyOne[i][0]+j*xDiv, polyOne[i][1]+j*yDiv]
            # samplePoint.append(a)
            precisePoint.append(a)
    return precisePoint


def write_text_file(finalPoi, fileName):
    f = open(fileName, 'w+')
    for i in finalPoi:
        for j in i:
            f.write(str(j[0]) + ',' + str(j[1]) + '\n')

        f.write("Next polygon \n")


# def lowest_lat_lon_with_OSM(nodeDATA, filename, osmID):
#     data = open_file(filename)
#     # print(nodeDATA)
#     lon_lat = []
#     for line in data:
#         testString = str.split(line, '~')
#         a = list(eval(testString[2]))
#         if testString[0] == osmID:
#             for i in a:
#                 lon_lat.append(get_lat_long(nodeDATA, i))
#                 # print(lon_lat)
#             break
#     # print(lon_lat)
#     lowestLatLon = getPointMinLat(lon_lat)
#     return lowestLatLon