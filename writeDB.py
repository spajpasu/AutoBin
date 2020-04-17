from importlib import reload
import Database
reload(Database)

b = Database.Database()
[conn, cur] = b.connectDB()
b.createIndex(cur)
b.writePath(cur)
b.dropIndex(cur)
b.disconnectDB(conn, cur)