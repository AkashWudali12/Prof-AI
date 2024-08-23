from typing import List
from pprint import pprint
import time
from author import AUTHOR
from get_profs_from_umd_directory import GET_PROFS_FROM_UMD_DIR
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModel
import torch
from langchain_core.documents import Document
import faiss
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
embeddings_model = AutoModel.from_pretrained("bert-base-uncased")

def embed_text(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Get the hidden states from the model
    with torch.no_grad():
        outputs = embeddings_model(**inputs)

    # Get the embeddings from the last hidden state
    embeddings = outputs.last_hidden_state

    # Aggregate embeddings (e.g., mean pooling)
    embeddings = torch.mean(embeddings, dim=1)

    return embeddings

def embed_documents(documents : List[Document]):
    embeddings = []
    for doc in documents:
        text = doc.__dict__["page_content"]  # Extract the text from the document
        embedding = embed_text(text)  # Get the embedding for the text
        embedding = embedding.tolist()
        embeddings.append(embedding)
    return np.array(embeddings, dtype='float32').tolist()

def main():
    start = time.time()

    umd_prof_finder = GET_PROFS_FROM_UMD_DIR()
    all_info = umd_prof_finder.extract_profs_information()

    author_collection_list = []

    for info in all_info:
        author_document = {}

        print("Author info", info)

        author = info["Name"]

        for key in info:
            author_document[key] = info[key]

        author_obj = AUTHOR(author_name=author)

        profile_page = author_obj.get_profile_page()

        print("Profile Page:", profile_page)

        articles_info = author_obj.get_abstracts()

        # articles_str = "\n".join([article["article_title"] + "\n" + article["article_abstract"] for article in articles_info])

        # author_document["Information About Articles"] = articles_str

        # text_splitter = RecursiveCharacterTextSplitter(chunk_size = 450, chunk_overlap=0)

        # documents = text_splitter.create_documents([articles_str])

        # embedding = embed_documents(documents)

        # author_document["embedding"] = embedding

        # for key in author_document:
        #     print(key)
        #     print("-"*50)
        #     print(author_document[key])
        
        # author_collection_list.append(author_document)

        quit()
    
    # insert into collection
    print("totalTime:", time.time()-start)

if __name__=="__main__":
    main()