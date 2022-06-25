import json
import random

f = open("products-with-id.json", "r")
productList = f.readlines()
f = open("products-with-price.json", "w")

fixedList = []
for i in range(len(productList)):
    jsondict = json.loads(productList[i])
    jsondict["Harga"] = random.randint(1, 500) * 10000
    toAppend = json.dumps(jsondict)
    f.write(toAppend)
    f.write("\n")
f.close()




