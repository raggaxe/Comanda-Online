import datetime

class BaseRepository():

    def __init__(self, conn):
        self.conn = conn['pet']


    def create(self, model):
        res = self.conn[model.collection_name].insert_one(model.__dict__)
        return self.find_one(model.collection_name, { '_id': res.inserted_id })

    def update_one(self, collection, query, new_data):
        new_data['updated_at'] = datetime.datetime.now()
        new_data  = {'$set': new_data}
        return self.conn[collection].find_one_and_update(query, new_data, return_document=True)

    def find(self, collection, query={}):
        return self.conn[collection].find(query)

    def find_one(self, collection, query):

        return self.conn[collection].find_one(query)

    def delete_one(self, collection, query):
        return self.conn[collection].delete_one(query)
