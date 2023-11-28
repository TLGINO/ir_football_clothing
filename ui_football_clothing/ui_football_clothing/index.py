import json

import pandas as pd
import pyterrier as pt


class Indexer:
    def __init__(self):
        if not pt.started():
            pt.init()

        self.index_path = "./football-clothing-index"
        self.data_path = "./data/data.csv"
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

        data_df = pd.concat(
            [
                adidas_df,
                decathlon_df,
                sports_direct_df,
            ]
        )

        data_df["docno"] = [str(i + 1) for i in range(len(data_df))]

        self.indexref = self.indexer.index(
            data_df["title"] + " " + data_df["data"],
            data_df["docno"],
        )

        data_df.to_csv(self.data_path)

        print("Data written to file.")

    def get_index_ref(self):
        return pt.IndexFactory.of(f"{self.index_path}/data.properties")

    def query_document_search(self, q=None, gte=None, lte=None):
        """
        Query documents by title and data for standard search.
        Optionally add a gte or lte price to the query.
        """
        query = [[str(i + 1), e] for i, e in enumerate(q.split(" "))]
        print(query)
        print(gte)
        print(lte)


        topics = pd.DataFrame(query, columns=["qid", "query"])

        self.indexref = self.indexref or self.get_index_ref()

        search_result_df = pt.BatchRetrieve(self.indexref).transform(topics)
        search_result_df["docno"] = search_result_df["docno"].astype(int)

        data_df = pd.read_csv(self.data_path)

        # Inner join the results
        result_df = data_df[data_df["docno"].isin(search_result_df["docno"])]

        if len(result_df) == 0:
            result_df = data_df.copy()
        
        if gte:
            result_df = result_df[result_df["price"] >= gte]
        if lte:
            result_df = result_df[result_df["price"] <= lte]

        result_df = result_df[["url", "title", "data", "price", "image"]]

        data = json.loads(result_df.to_json(orient="records"))

        return data


if __name__ == "__main__":
    indexer = Indexer()
    indexer.setup_index()
    # res = indexer.query_document_search(q="nike")
    # print(res)
    # print(len(res))
