import json

f = open("products-with-id.json", "r")
prodlist = f.readlines()
jsonlist = []

# convert to dict
for item in prodlist :
    jsonlist.append(json.loads(item))

# # get unique categories
# f = open("categories.txt", "w")
# catset = set()
# for record in jsonlist:
#     catset.add(record["Kategori"])

# for cat in catset:
#     f.write(cat+",")
# f.close()
    
g = open ("categories.txt", "r")
catlist = g.readline().split(",")
cat_id_dict = {}
for cat in catlist:
    idlist = []
    for record in jsonlist:
        if record["Kategori"] == cat:
            idlist.append(record["id"])
    cat_id_dict[cat] = idlist

thestring  = json.dumps(cat_id_dict)

g = open("catlist.json", "w")
g.write(thestring)
g.close()

g = open("catlist.json", "r")
strink = g.readline()
print(strink)
