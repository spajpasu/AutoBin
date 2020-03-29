from importlib import reload

import psycopg2
import InputData
reload(InputData)

from InputData import InputData

id = "'543.265.189'" # should be unique
name = "'Building_1234'"
point = "'POINT(3 7)'"
# polygon = "'POLYGON((1 2, 6 1, 9 3, 7 5, 3 6, 1 2))'"
polygon = "'MULTIPOLYGON(((1 2, 6 1, 9 3, 7 5, 3 6, 1 2)), ((4 9, 7 6, 9 8, 4 9)))'"
path = "'D:\\UniDuE\\hiwi\\AutoBin\\Project_Files\\01_Blender\\osm2postgre\\Dortmund_small_test.osm'"

conn = psycopg2.connect(host = InputData().hostName, database = InputData().databaseName,
                       user = InputData().userName, password = InputData().passwordSec)

cur = conn.cursor()

# cur.execute("CREATE TABLE %s (vendor_id SERIAL PRIMARY KEY, vender_name text NOT NULL)" %InputData().tableName)

# print('%s' %'text')
# cur.execute("INSERT INTO test(vender_name) VALUES(%s) RETURNING vendor_id;" %"\'Kumar\'")
cur.execute("INSERT INTO %s(osm_id, osm_name, osm_polygon, osm_point, file_path) VALUES(%s, %s, %s, %s, %s);"
            %(InputData().tableName, id, name, polygon, point, path))
# row = cur.fetchall()
# for r in row:
#     print(f"id {r[0]} name {r[1]}")
print("Row inserted")

# print('Table with name %s created.' %InputData().tableName)

cur.close()
conn.commit()
conn.close()