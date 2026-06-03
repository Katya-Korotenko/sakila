from typing import Any
from mongo_connector import get_mongo_collection


class Statistic:
    """Executes aggregation and metric extraction from telemetry datasets in MongoDB."""

    def __init__(self) -> None:
        """Establishes reference connection pointer to the analytical logs database collection."""
        self.collection = get_mongo_collection()

    def get_top_searches(self) -> list[dict[str, Any]]:
        """Assembles the top 5 most frequently dispatched search input variations."""
        return list(self.collection.aggregate([
            {'$group': {'_id': '$params', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 5}
        ]))