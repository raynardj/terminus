from pymongo import MongoClient
def get_db(database):
	"""
	A quick way to get MongoDb Client link
	"""
	clientmg=MongoClient()
	db=clientmg[database]
	return db
db=get_db("foundation")
plist=db.process.find({},{"price":1,"qtt":2})
for p in plist:
	ttlamt=float(float(p["price"])*float(p["qtt"]))
	db.process.update({"_id":p["_id"]},{"$set":{"ttlamt":ttlamt}},upsert=True)