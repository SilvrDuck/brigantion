import pymongo

user = 'root'
pwd = 'password'
host = 'localhost'
port = '27017'

conn = pymongo.MongoClient(host = f'mongodb://{user}:{pwd}@{host}:{port}/')
db = conn.brigantion
