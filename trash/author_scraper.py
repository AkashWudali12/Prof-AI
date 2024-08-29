import requests
import json
import pprint
from dotenv import load_dotenv
import os
import json
from googleapiclient.discovery import build

# URL you want to make a GET request to

load_dotenv("my_env.env")
api_key = os.environ['GOOGLE_API_KEY']
search_engine_id = "e6a0456e3f63b45e5"

payload = {
    'key':api_key
}

class AUTHOR_SCRAPER:
    def __init__(self, author_ID):
        self.author_id = author_ID
    
    def get_author_information_json(self):
        authors_url = "https://serpapi.com/search?engine=google_scholar_author"


        # set serp api key as environment varible
        params = {
        "api_key": api_key,
        "author_id": self.author_id,
        }

        response = requests.get(authors_url, params)

        if response.status_code == 200:
            data = response.json()
            print("Got Data")
            return data
        else:
            print("Failed to retrieve data:", response.status_code)
            print("Message", response.json())
            return None
    
    def get_article_links(self):
        new_list = []
        try:
            articles_dict = self.get_author_information_json()["articles"]
            for article in articles_dict:
                if "link" in article:
                    new_list.append(article["link"])
        except:
            print("Error Occured: Cannot Extract Links")
        return new_list
    
    def get_article_names(self, author_information_json):
        titles = []
        articles_list = author_information_json["articles"]
        for article in articles_list:
            titles.append(article["title"])
        return titles
            
    
    def remove_links(self, articles_dict):
        new_list = []
        # should be output_from_author_information["articles"]
        for article in articles_dict:
            if "link" in article:
                del article["link"]
            if "cited_by" in article:
                del article["cited_by"]
            new_list.append(article)
        return new_list


