from pymongo import MongoClient

CONN_ = "mongodb+srv://Ulyana:6894@ulyanahw10.3uxoc.mongodb.net/UlyanaHW10?retryWrites=true&w=majority"
client = MongoClient(CONN_)

db = client.addressbook
