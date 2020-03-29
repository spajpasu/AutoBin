from importlib import reload

import InputData
import psycopg2
reload(InputData)
from InputData import InputData

class Database:

    def connectDB(self):
        try:
            conn = psycopg2.connect(host=InputData().hostName, database=InputData().databaseName,
                                user=InputData().userName, password=InputData().passwordSec)
            cur = conn.cursor()
            print("Connection to database successful...")
            return conn, cur
        except Exception as error:
            print("Connection to database not successful. Error: ", error)
            print("EXCEPTION TYPE: ", type(error))

    def writePath(self, conn, cur):
        f = open(InputData().objName+'.txt', "r")
        i = ''
        for x in f:
            l = x.strip().split("\t")
            cur.execute(
                "SELECT file_path FROM {} WHERE osm_id = {};".format(InputData().tableName, int(l[0])))
            val = cur.fetchone()
            if val[0] == None or val[0] == 'NULL':
                cur.execute(
                    "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
            else:
                if i == 'yes':
                    cur.execute(
                        "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
                else:
                    res = self.decisionCheck()
                    if res == 'y' or res == 'yes':
                        cur.execute(
                            "UPDATE {} SET file_path = \'{}\' WHERE osm_id = {};".format(InputData().tableName, l[1], int(l[0])))
                        i = res
                    else:
                        print('The value in DataBase has not changed.')
        f.close()

    def decisionCheck(self):
        print('The value at {} is already full'.format('file_path'))
        decision = input("Do you want to overwrite data y/n ? \n to save result and process for all, press 'yes'.\n")
        if decision == 'y':
            return decision
        elif decision == 'yes':
            return decision
        else:
            return decision

    def disconnectDB(self, conn, cur):
        cur.close()
        conn.commit() # write this in insert
        conn.close()
