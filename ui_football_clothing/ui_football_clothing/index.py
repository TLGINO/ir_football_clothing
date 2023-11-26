import json

from opensearchpy import OpenSearch


class Indexer:
    def __init__(self):
        self.host = "localhost"
        self.port = 9200
        self.auth = (
            "admin",
            "admin",
        )
        self.client = self.__init_connection()
        self.__setup_index()

    def __init_connection(self):
        """Connect to OpenSearch instance."""
        return OpenSearch(
            hosts=[{"host": self.host, "port": self.port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def __setup_index(self):
        """Create and populate index."""
        index_name = "football-clothing-index"
        index_body = {
            "settings": {"number_of_shards": 1, "number_of_replicas": 1},
            "mappings": {
                "properties": {
                    "url": {"type": "text"},
                    "title": {"type": "text"},
                    "data": {"type": "text"},
                    "price": {"type": "integer"},
                    "image": {"type": "text"},
                }
            },
        }
        try:
            self.client.indices.create(index_name, body=index_body)
            print("Index Created!")

            print("Bulk Indexing Data (1/3):")
            self.index_document_bulk("../data/adidas.json")

            print("Bulk Indexing Data (2/3):")
            self.index_document_bulk("../data/decathlon.json")

            print("Bulk Indexing Data (3/3):")
            self.index_document_bulk("../data/sports_direct.json")
            print("Done")

        except Exception as e:
            print("Error creating index, does index already exist?")
            print(e)

    def index_document_bulk(self, document_path):
        """Index a json document."""
        data = json.load(open(document_path))

        bulk_document = "".join(
            [
                '{ "index" : { "_index" : "football-clothing-index" } } \n '
                + json.dumps(d)
                + " \n "
                for d in data
            ]
        )
        self.client.bulk(bulk_document)

    def query_document_search(self, q):
        """Query documents by title and data for standard search."""
        query = {
            "size": 10,
            "query": {"multi_match": {"query": q, "fields": ["title^2", "data"]}},
        }
        response = self.client.search(body=query, index="football-clothing-index")
        return response["hits"]["hits"]

    def query_document_price(self, q):
        """Query documents by price for recommendation."""
        query = {
            "size": 10,
            "query": {"multi_match": {"query": q, "fields": ["price"]}},
        }
        response = self.client.search(body=query, index="football-clothing-index")
        return response["hits"]["hits"]


if __name__ == "__main__":
    indexer = Indexer()
