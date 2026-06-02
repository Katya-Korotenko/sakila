from  mongo_connector import get_mongo_collection


class Statistic:

    def __init__(self):
        self.collection = get_mongo_collection()

    def get_top_searches(self):
        return list(self.collection.aggregate([
            {'$group': {'_id': '$params', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 5}
        ]))
