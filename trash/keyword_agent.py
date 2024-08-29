"""
The keyword agent takes a description of a user's interests and condenses it into keywords
"""
import os
import json
from typing import List, Dict
import pymongo
from dotenv import load_dotenv
import time
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
# from openai import AzureOpenAI

# from openai import AzureOpenAI
# from tenacity import retry, wait_random_exponential, stop_after_attempt
# import numpy as np
# from langchain.schema.runnable import Runnable
# from langchain.embeddings import AzureOpenAIEmbeddings
# from langchain.vectorstores.azure_cosmos_db import AzureCosmosDBVectorSearch
# from langchain.schema.document import Document
# from langchain.agents import Tool
# from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
# import faiss

load_dotenv("my_env.env")
AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
AOAI_API_VERSION = "2023-09-01-preview"
COMPLETIONS_DEPLOYMENT = "completions"
EMBEDDINGS_DEPLOYMENT = "embeddings"

class KeywordAIAgent:
    def __init__(self):

        self.system_message = SystemMessage(
            content = 
            
            """
            You're here to pinpoint relevant keywords from the user's descriptions of their academic interests. 
                        
            You will analyze the user's input and provide a list of 2 keywords in one line seperated by commas
            """
        )

        print(AOAI_KEY)

        self.agent = AzureChatOpenAI(
            openai_api_version=AOAI_API_VERSION,
            azure_deployment=COMPLETIONS_DEPLOYMENT,
            api_key=AOAI_KEY,
            azure_endpoint=AOAI_ENDPOINT)

    def run(self, prompt: str) -> str:
        """
        Run the AI agent.
        """

        messages = [
            HumanMessage(
                content=prompt
            ),
            SystemMessage(
                content=self.system_message.content
            )
        ]

        result = self.agent.invoke(messages)

        return result.content

    def placeholder_method(self):
        return 1



# prompt llm to match research interests