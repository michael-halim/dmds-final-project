import sqlite3

from numpy import product
import mongoconnect
import neo4jconnect as neo
import os
from dotenv import load_dotenv
load_dotenv()

sqlite_client = sqlite3.connect("session_database.db")
mongo_client = mongoconnect.PyMongoClient( "mongodb://localhost:27017/", "proyek-dmds", "products-final")
neo4j_client = neo.Neo4jConnector("bolt://localhost:7687", os.environ.get('USER_NEO4J'), os.environ.get('PASSWORD_NEO4J'))

cursor = sqlite_client.cursor()
# create new table
sql_query = "DROP TABLE IF EXISTS profit_data"
cursor.execute(sql_query)
sql_query = "CREATE TABLE IF NOT EXISTS profit_data([profit_id] INT, [transaction_id] INT, [user_id] INT, [contributor_id] INT, profit_amount[INT])"
cursor.execute(sql_query)

# open the transaction_details
sql_query = "SELECT * FROM transaction_details"
cursor.execute(sql_query)
transaction_details = cursor.fetchall()

profit_details = []
profit_id = 0
for i in range(len(transaction_details)):
    transaction_record = transaction_details[i]
    product_price = mongo_client.getPriceByID(transaction_record[3])[0]["Harga"]
    product_qty = transaction_record[4]
    total = product_price * product_qty

    # 80% goes to company
    transaction_id = transaction_record[0]
    user_id = 8 # for some reason company is no 8
    contributor_id = transaction_record[1]
    profit_amount = 0.8 * total
    profit_details.append(tuple([profit_id, transaction_id, user_id, contributor_id, profit_amount]))

    profit_id += 1
    # the remaining 20% is split among the forefathers with patterns
    # 50 30 20 | 50 50 | 100 depending on how many forefathers
    forefathers = neo4j_client.get_shortest_path_by_ID(contributor_id)
    # exclude self
    forefathers.pop(0)

    # by case
    if len(forefathers) == 1:
        profit_amount = 0.2 * total
        profit_details.append(tuple([profit_id,transaction_id, forefathers[0], contributor_id, profit_amount]))
        profit_id += 1
    if len(forefathers) == 2:
        profit_amount = 0.1 * total
        profit_details.append(tuple([profit_id, transaction_id, forefathers[0], contributor_id, profit_amount]))
        profit_details.append(tuple([profit_id + 1, transaction_id, forefathers[1], contributor_id, profit_amount]))
        profit_id += 2
    if len(forefathers) >= 3:
        real_forefathers = forefathers[0:3]
        profit_details.append(tuple([profit_id, transaction_id, real_forefathers[0], contributor_id, 0.1 * total]))
        profit_details.append(tuple([profit_id + 1, transaction_id, real_forefathers[1], contributor_id, 0.06 * total]))
        profit_details.append(tuple([profit_id + 2, transaction_id, real_forefathers[2], contributor_id, 0.04 * total]))
        profit_id += 3

# insert to the table
for record in profit_details:
    sql_query = "INSERT INTO profit_data VALUES(?,?,?,?,?)"
    cursor.execute(sql_query, (record[0], record[1], record[2], record[3], record[4]))

sqlite_client.commit()