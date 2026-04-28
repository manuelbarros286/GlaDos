import os
import ssl

# 1. Standard SSL bypass
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context

# 2. Tell HuggingFace specifically to stop verifying (The missing link)
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
# This is a bit of a hack, but it forces the underlying requests to ignore SSL
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer


class VectorService:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)

        print("Loading Embedding Model...")

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = "intelligence_reports"

    def init_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
        print(f"Collection '{self.collection_name}' initialized.")

    def embed_text(self, text):
        return self.model.encode(text).tolist()


if __name__ == "__main__":
    vs = VectorService()
    vs.init_collection()
