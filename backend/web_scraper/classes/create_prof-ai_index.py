from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

import itertools
import time
import tqdm
from sentence_transformers import SentenceTransformer
from pprint import pprint

import json
import os

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)

pc.create_index(
    name="prof-ai",
    dimension=768, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)