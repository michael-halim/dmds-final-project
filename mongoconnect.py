import pymongo

class PyMongoClient():
    
    def __init__(self, uri, db, col):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db]
        self.col = self.db[col]

    def close(self):
        self.client.close()

    def getAll(self):
        return self.col.find()
    
    def getAllShort(self):
        return self.col.find({}, {"_id":0, "id":1,  "Nama" : 1, "Kategori":1, "Brand" : 1, "Harga" : 1})
    
    def getAllByID(self,id_p):
        return self.col.find({"id":id_p},{"_id" : 0})
    
    def getPriceByID(self, id):
        return self.col.find({"id":id},{"_id" : 0, "Harga" : 1})

    def getDetailByID(self, id):
        return self.col.find_one({"id":id},{"_id" : 0, "Harga" : 1, "Nama" : 1, "Brand":1})

    def printAll(self):
        myDict = self.getAll()
        for record in myDict:
            print("__________________________")
            for key in record:
                print(key," : ", record[key])
    
    def printAllShort(self):
        myDict = self.getAllShort()
        for record in myDict:
            print("__________________________")
            for key in record:
                print(key," : ", record[key])
                
    def printPrice(self, id):
        myDict = self.getPriceByID(id)
        for record in myDict:
            print("_________________________")
            for key in record:
                print(key," : ", record[key])


        
myclient = PyMongoClient("mongodb://localhost:27017/", "proyek-dmds", "products-final")