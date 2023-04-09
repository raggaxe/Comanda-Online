import pymongo
import os

class MongoConfig():

    def __init__(self):
        # mongo_uri = os.getenv('DATABASE_URL')
        # self.conn = pymongo.MongoClient(mongo_uri)
        self.conn = pymongo.MongoClient('localhost', 27017)

    def get_connect(self):
        return self.conn

