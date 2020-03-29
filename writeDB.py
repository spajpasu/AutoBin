from importlib import reload
import Database
reload(Database)

b = Database.Database()
[conn, cur] = b.connectDB()
b.writePath(conn, cur)
b.disconnectDB(conn, cur)