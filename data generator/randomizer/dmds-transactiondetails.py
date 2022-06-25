import random
import sqlite3
import json

# accepts a person's actions that has purchased and makes some details
def makeTransactionDetail(index, session_data):
    global id
    global catlist # QOL improvement since i know this applies in python
    # find a "cart.php" and assume that the item before it is bought
    for i in range(len(session_data)):
        print(session_data[i])
        if session_data[i][2] == "cart.php":
            category = session_data[i-1][2] # previous session's category
            product_id = random.choice(catlist[category])
            qty = random.randint(1, 5)
            c.execute(''' 
                INSERT INTO transaction_details VALUES(?,?,?,?,?)
            ''', (id, session_data[i][0], session_data[i][1], product_id, qty))
            id += 1
    db.commit()
                
# open the dict
f = open("catlist.json", "r")
strink = f.readline()
catlist = json.loads(strink)

db = sqlite3.connect("session_database.db")
c = db.cursor()
# make the table if not there already
c.execute("DROP TABLE IF EXISTS transaction_details")
c.execute("CREATE TABLE IF NOT EXISTS transaction_details([transaction_id] INT, [user_id] INT, [timestamp] TEXT, [product_id] INT, [qty] INT) ")
id = 1

# now get each user and detect if he buys
for i in range(1, 262+1):
    c.execute("SELECT user_id, timestamp, activity FROM session_data WHERE user_id ={}".format(i))
    oneman = c.fetchall()
    # if he purchases, make the details
    for record in oneman:
       if record[2] == "checkout.php":
        makeTransactionDetail(i, oneman)
