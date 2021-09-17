from pymongo import MongoClient

CONN_ = "mongodb+srv://...:...@ulyanahw10.3uxoc.mongodb.net/...?retryWrites=true&w=majority"
client = MongoClient(CONN_)

db = client.addressbook

import redis 
redis_db = redis.Redis(host = 'localhost', port = 6379, db = 0)

list_cache = list(redis_db.scan_iter())