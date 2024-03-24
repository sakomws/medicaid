# set up Fireworks.ai Key
import os
import requests
import json
from datasets import load_dataset
import pandas as pd

fw_api_key = os.environ["FIREWORKS_API_KEY"]

from datasets import load_dataset
import pandas as pd

# https://huggingface.co/datasets/AIatMongoDB/whatscooking.restaurants
dataset = load_dataset("goup/medicaid")

# Convert the dataset to a pandas dataframe
dataset_df = pd.DataFrame(dataset["train"])

from llama_index.core.settings import Settings
from llama_index.llms.fireworks import Fireworks
from llama_index.embeddings.fireworks import FireworksEmbedding

embed_model = FireworksEmbedding(
    embed_batch_size=512,
    model_name="nomic-ai/nomic-embed-text-v1.5",
    api_key=fw_api_key,
)
llm = Fireworks(
    temperature=0,
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    api_key=fw_api_key,
)

Settings.llm = llm
Settings.embed_model = embed_model

import json
from llama_index.core import Document
from llama_index.core.schema import MetadataMode

# Convert the DataFrame to a JSON string representation
documents_json = dataset_df.to_json(orient="records")
# Load the JSON string into a Python list of dictionaries
documents_list = json.loads(documents_json)

llama_documents = []

for document in documents_list:
    # Value for metadata must be one of (str, int, float, None)
    document["instruction"] = json.dumps(document["instruction"])
    document["context"] = json.dumps(document["context"])
    document["response"] = json.dumps(document["response"])
    document["category"] = json.dumps(document["category"])

    # Create a Document object with the text and excluded metadata for llm and embedding models
    llama_document = Document(
        text=json.dumps(document),
        metadata=document,
        metadata_template="{key}=>{value}",
        text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
    )

    llama_documents.append(llama_document)

# # Observing an example of what the LLM and Embedding model receive as input
# print(
#     "\nThe LLM sees this: \n",
#     llama_documents[0].get_content(metadata_mode=MetadataMode.LLM),
# )
# print(
#     "\nThe Embedding model sees this: \n",
#     llama_documents[0].get_content(metadata_mode=MetadataMode.EMBED),
# )

llama_documents[0]

from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(llama_documents)
# 25k nodes takes about 10 minutes, will trim it down to 2.5k
new_nodes = nodes[:2500]

# There are 25k documents, so we need to do batching. Fortunately LlamaIndex provides good batching
# for embedding models, and we are going to rely on the __call__ method for the model to handle this
node_embeddings = embed_model(new_nodes)

for idx, n in enumerate(new_nodes):
    n.embedding = node_embeddings[idx].embedding
    if "_id" in n.metadata:
        del n.metadata["_id"]

import pymongo


def get_mongo_client(mongo_uri):
    """Establish connection to the MongoDB."""
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None


# set up Fireworks.ai Key
import os
import getpass

mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    print("MONGO_URI not set")

mongo_client = get_mongo_client(mongo_uri)

DB_NAME = "hipaa-db"
COLLECTION_NAME = "medicaid"

db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.delete_many({})

from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

vector_store = MongoDBAtlasVectorSearch(
    mongo_client,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME,
    index_name="vector_index",
)
vector_store.add(new_nodes)

from llama_index.core import VectorStoreIndex, StorageContext

index = VectorStoreIndex.from_vector_store(vector_store)

query_engine = index.as_query_engine()
query = "search query: What is the annual income of the applicant?"

response = query_engine.query(query)
print(response)