import random
import sqlite3
from datetime import date, datetime, timedelta
from dateutil import parser

behavior_list = [
    "browse-nobuy",
    "browse-buy-one",
    "browse-buy-many",
    "buy-one",
]
seconds_offset = [1, 60, 3600]
category_list = [
    "Sofa Bed",
    "Sofa 2 Seater",
    "Sofa 3 Seater",
    "Kursi Ottoman & Stool",
    "Sofa Bed",
    "Meja Tamu",
    "Nakas",
    "Meja Kerja",
    "Kursi Kantor",
    "Meja TV",
    "Rak Buku & Rak Display",
    "Credenza",
    "Rak Sepatu",
    "Lemari Laci",
    "Standing Mirror",
    "Tempat Tidur Single",
    "Tempat Tidur Queen",
    "Tempat Tidur King",
    "Kursi Makan",
    "Meja Makan",
    "Kursi Panjang",
    "Kabinet Dapur",
    "Meja TV",
]

id = 1000
index = 0
user = 1
date_seed = datetime.now()

def makeRecord(user_id, act):
    global id
    global date_seed
    global index

    record = []
    # index
    record.append(index)
    # session id
    record.append(id + index)
    index += 1

    # user id
    record.append(user)

    # timestamp
    timeOffsetMajor = seconds_offset[random.randint(0, 2)]
    if(timeOffsetMajor != 3600):
        timeOffsetMajor *= random.randint(0, 59)
        timeOffsetMajor += random.randint(0, 59)
    thisDate = '{:%Y-%m-%d %H:%M:%S}'.format(
        date_seed + timedelta(seconds=timeOffsetMajor))
    record.append(thisDate)
    date_seed = parser.parse(thisDate)

    # activity
    if act == "login":
        record.append("home.php")
    elif act == "cart":
        record.append("cart.php")
    elif act == "browse":
        random_cat = random.choice(category_list)
        record.append(random_cat)
    elif act == "purchase":
        record.append("checkout.php")

    # category
    record.append(act)
    return record

def makeActivity(behavior):
    global mylist
    global user
    global date_seed

    # behavior type
    if behavior == "browse-nobuy":
        # login
        mylist.append(makeRecord(user, "login"))
        # browses many categories
        times = random.randint(1, 10)
        for i in range(times):
            mylist.append(makeRecord(user, "browse"))

    elif behavior == "browse-buy-one":
        # login
        mylist.append(makeRecord(user, "login"))
        # browses many categories
        times = random.randint(1, 10)
        for i in range(times):
            mylist.append(makeRecord(user, "browse"))
        # carts once
        mylist.append(makeRecord(user, "cart"))
        # buys it
        mylist.append(makeRecord(user, "purchase"))

    elif behavior == "browse-buy-many":
        # login
        mylist.append(makeRecord(user, "login"))
        # browses many categories
        times = random.randint(1, 10)
        cartCounter = 0
        for i in range(times):
            mylist.append(makeRecord(user, "browse"))
            # may cart an item
            if random.randint(0, 100) > 50:
                mylist.append(makeRecord(user, "cart"))
                cartCounter+= 1
            #carts a minimal of one item
            if cartCounter == 0:
                mylist.append(makeRecord(user, "cart"))
            
        # has a slight chance of not buying it
        if random.randint(0, 100) > 10:
            mylist.append(makeRecord(user, "purchase"))

    elif behavior == "buy-one":
        # login
        mylist.append(makeRecord(user, "login"))
        # goes to one category
        mylist.append(makeRecord(user, "browse"))
        # buys it
        mylist.append(makeRecord(user, "cart"))
        mylist.append(makeRecord(user, "purchase"))

    # after one man sequence, increment user and pick a random time for the next person
    user += 1
    date_seed = date_seed = parser.parse(
        mylist[random.randint(0, len(mylist) - 1)][3])

mylist = []
# some users users
people = 99
print("there are ", people)
for i in range(people):
    # logs a user with a certain behavior
    behavior_type = random.choice(behavior_list)
    makeActivity(behavior_type)
    # a chance to advance the day
    if random.randint(0, 100) < 10:
        date_seed += timedelta(days=1, hours=random.randint(0, 12))

mylist.sort(key=lambda x: x[3])
# hard rearrange
for i in range(len(mylist)):
    mylist[i][0] = i
    mylist[i][1] = i + id

# # time 4 mysql
db = sqlite3.connect('session_database.db')
c = db.cursor()

# create the table if it aint there yet
c.execute('''
        DROP TABLE IF EXISTS session_data
''')
c.execute('''
          CREATE TABLE IF NOT EXISTS session_data
          ([index] INT, [session_id] INT, [user_id] INT, [timestamp] TEXT, [activity] TEXT, [category] TEXT)
          ''')

for record in mylist:
    c.execute('''
            INSERT INTO session_data VALUES (?,?,?,?,?,?)
    ''',(record[0], record[1], record[2], record[3], record[4], record[5]))
db.commit()
