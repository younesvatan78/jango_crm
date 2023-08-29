import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'YpCqU46689'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE jango_test")
print("done")
