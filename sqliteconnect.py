import sqlite3

db = sqlite3.connect("session_database.db")
cursor = db.cursor()

query = ""
cursor.execute(query)
db.commit()
db.close()