from datetime import datetime
from typing import Any
from mongo_connector import get_mongo_collection


class SearchLogger:
    """Manages appending search logging transactions to MongoDB."""

    def __init__(self) -> None:
        """Establishes reference connection pointer to the target MongoDB logs collection."""
        self.collection = get_mongo_collection()

    def log_search(self, search_type: str, params: dict[str, Any], results_count: int) -> None:
        """Appends a new structured log document to the search history collection.

        Args:
            search_type: The logical classification of search performed.
            params: The collection of key-value user inputs applied to the query.
            results_count: The quantity of matching objects captured on the first page.
        """
        document: dict[str, Any] = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }
        self.collection.insert_one(document)