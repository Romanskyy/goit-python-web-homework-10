from pymongo import MongoClient

CONN_ = "mongodb+srv://...:...@ulyanahw10.3uxoc.mongodb.net/...?retryWrites=true&w=majority"
client = MongoClient(CONN_)

db = client.addressbook
