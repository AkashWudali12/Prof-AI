import os
import openai
from web_scraper.classes.prof_ai_agent import ProfAIAgent
import random

from pprint import pprint  # This imports the function pprint from the pprint module
# maybe switch to perplexity in the future

author_name = "Percy Liang"

author_information_json = "" # information about author

agent = ProfAIAgent()

prompt = "You are emailing Professor"  + author_name + "\n" """

Generate a cold email reaching out to the proffesor for potential opportunities working as a research assistant.
Information about their publications is specified in the printed JSON file. 
Don't cite specific articles, but ensure to include specific information about the professor's research topics and interests.
Also mention how I met with him at a recent conference.

Do not use your tools

""" + "\n" + str(author_information_json["articles"])

agent_output = agent.run(prompt)

print("CHAIN FINISHED")

print("-----------------------------")

print(agent_output)

print("-----------------------------")
