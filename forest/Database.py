from importlib import reload

import InputData
import psycopg2
reload(InputData)
import InputData

class Database:

    def connectDB(self):
        try:
            conn = psycopg2.connect(host=InputData.hostName, database=InputData.databaseName,
                                user=InputData.userName, password=InputData.passwordSec)
            cur = conn.cursor()
            print("Connection to database successful...")
            return conn, cur
        except Exception as error:
            print("Connection to database not successful. Error: ", error)
            print("EXCEPTION TYPE: ", type(error))


    def insertDATA(self, cursor, query):
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as error:
            print("Failed to insert record into {} table {}".format(InputData.tableName, error))

    def createIndex(self, cursor):
        cursor.execute(
            "CREATE INDEX osm_id_index ON {} (osm_id);".format(InputData.tableName))


    def id_check_execute(self, cursor, osm_val):
        query = "SELECT osm_point FROM {} WHERE  osm_id = {};"\
            .format(InputData.tableName, osm_val)
        cursor.execute(query)
        return cursor.fetchone() is not None

    # def writePath(self, cur):
    #     f = open(InputData.objName+'.txt', "r")
    #     i = ''
    #     for x in f:
    #         l = x.strip().split("\t")
    #         cur.execute(
    #             "SELECT file_path FROM {} WHERE osm_id = {};".format(InputData().tableName, int(l[0])))
    #         val = cur.fetchone()
    #         if val[0] == None or val[0] == 'NULL':
    #             cur.execute(
    #                 "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
    #         else:
    #             if i == 'yes':
    #                 cur.execute(
    #                     "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
    #             else:
    #                 res = self.decisionCheck()
    #                 if res == 'y' or res == 'yes':
    #                     cur.execute(
    #                         "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
    #                     i = res
    #                 else:
    #                     print('The value in DataBase has not changed.')
    #     f.close()

    def decisionCheck(self, osm_id):
        print('A value with {} already exists'.format(osm_id))
        decision = input("Do you want to overwrite data y/n ? \n to save result and process for all, press 'yes'.\n")
        if decision == 'y':
            return decision
        elif decision == 'yes':
            return decision
        else:
            return decision

    def dropIndex(self, cursor):
        cursor.execute("DROP INDEX osm_id_index;")

    def disconnectDB(self, conn, cur):
        cur.close()
        conn.commit() # write this in insert
        conn.close()
