from datetime import datetime
from mongo_connector import get_mongo_collection


class SearchLogger:

    def __init__(self):
        self.collection = get_mongo_collection()

    def log_search(self, search_type, params, results_count):
        document = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count}

        self.collection.insert_one(document)



