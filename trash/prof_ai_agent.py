"""
The Prof_ai_agent class creates an agent that generated cold emails to professors 
Promot should include information about the author
"""
import os
import json
from typing import List, Dict
import pymongo
from dotenv import load_dotenv
import time
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
import tiktoken as tk
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


class ProfAIAgent:
    def __init__(self, system_message : SystemMessage):

        self.system_message = system_message

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

    def generate_cold_email(self, author_name, abstract_article_list):

        system_prompt = "You are emailing Professor "  + author_name + "\n" """

        Generate a cold email reaching out to the proffesor for potential opportunities working as a research assistant.
        Information about their publications and abstracts are below. Don't use too overzelous wording.
        Don't cite specific articles, but ensure to include specific information about the professor's research topics and interests.

        Do not use your tools

        """

        encoding = tk.encoding_for_model("gpt-3.5-turbo")

        while abstract_article_list and len(encoding.encode(system_prompt)) < 3500:
            new_prompt = system_prompt + "\n" + str(abstract_article_list.pop(0))
            if len(encoding.encode(new_prompt)) < 3500:
                system_prompt = new_prompt
        
        output = self.run(prompt=system_prompt)

        return output

    def placeholder_method(self):
        return 1



# prompt llm to match research interests