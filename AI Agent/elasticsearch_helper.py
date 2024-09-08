from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch.exceptions import ElasticsearchException  # Correct import for exceptions


# Helper function to initialize Elasticsearch client
def create_elasticsearch_client():
    try:
        client = Elasticsearch("http://localhost:9200")
        if not client.ping():
            raise ValueError("Connection failed.")
        return client
    except ElasticsearchException as e:
        print(f"Error creating Elasticsearch client: {e}")
        raise

# Function to retrieve relevant documents using BM25
def retrieve_relevant_docs(query, index="content-index", field="content", size=3):
    try:
        es = create_elasticsearch_client()
        res = es.search(index=index, body={
            "query": {
                "match": {
                    field: query
                }
            },
            "size": size  # Limit the number of returned documents
        })
        documents = [hit["_source"].get(field, "No content available") for hit in res["hits"]["hits"]]
        return " ".join(documents)
    except ElasticsearchException as e:
        print(f"Error retrieving documents: {e}")
        return ""
