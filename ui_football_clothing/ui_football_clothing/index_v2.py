import json

import pandas as pd
import pyterrier as pt


class Indexer:
    def __init__(self):
        if not pt.started():
            pt.init()

        self.index_path = "./football-clothing-index"
        self.indexer = pt.DFIndexer(
            index_path=self.index_path, overwrite=True, verbose=True
        )
        self.indexref = None

    def setup_index(self):
        """Create and populate index."""

        print("Bulk Indexing Data:")

        adidas_df = pd.read_json("../data/adidas.json")
        decathlon_df = pd.read_json("../data/decathlon.json")
        sports_direct_df = pd.read_json("../data/sports_direct.json")

        result_df = pd.concat(
            [
                adidas_df,
                decathlon_df,
                sports_direct_df,
            ]
        )

        result_df["docno"] = [str(i + 1) for i in range(len(result_df))]

        self.indexref = self.indexer.index(
            result_df["url"],
            result_df["title"],
            result_df["data"],
            # result_df["price"],
            result_df["image"],
            result_df["docno"],
        )

    def query_document_search(self, q=None, gte=None, lte=None):
        """
        Query documents by title and data for standard search.
        Optionally add a gte or lte price to the query.
        """
        topics = pd.DataFrame(
            [["1", "adidas"], ["2", "shirt"]], columns=["qid", "query"]
        )
        res = pt.BatchRetrieve(self.indexref).transform(topics)
        print(res)
        res.to_csv("res.csv")
        exit()

        query = {"size": 1000, "fields": ["url", "title", "data", "price", "image"]}

        if q:
            query["text"] = q

        if gte or lte:
            query["controls"] = {"pricemin": gte, "pricemax": lte}

        if not q and not gte and not lte:
            query["text"] = "*"

        result = self.indexer.search(**query)
        return result


if __name__ == "__main__":
    indexer = Indexer()
    indexer.setup_index()
    res = indexer.query_document_search(q="shirt")
    # print(res)
