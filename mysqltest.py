import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "mysql_test"
    
)

c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS testtable(attribute1 int(5), attribute2 varchar(50))")
 