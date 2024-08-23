import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import random

class HUMAN_REQUEST:
    def __init__(self, url):
        self.url = url

    def get_response(self):
        # Using sessions to maintain cookies and headers across requests

        ua = UserAgent()
        self.headers = {
                'User-Agent': ua.random
            }

        with requests.Session() as session:
            session.headers.update(self.headers)

            try:
                response = session.get(self.url)
                # print(response.text)  # This will print the HTML content of the page

                # To mimic human-like intervals between requests
                time_for_request = random.randint(20, 100)
                print("Time for request:", time_for_request)
                time.sleep(time_for_request)  

            except requests.exceptions.RequestException as e:
                response = ""
                print("Request failed: ", e)
        return response

    def get_soup(self):
        try: 
            response = self.get_response()
            if response:
                print("Got Response")
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except Exception as e:
            print("Get Soup Failed:", e)
            return ""
    
    """
    def human_google_search_soup(self, query, num_results):
        params = {
            "q": query, # query example
            "hl": "en",          # language
            "gl": "us",          # country of the search, UK -> United Kingdom
            "start": 0,          # number page by default up to 0
            "num": num_results          # parameter defines the maximum number of results to return.
        }

        with requests.Session() as session:
            session.headers.update(self.headers)

            try:
                response = session.get(self.url, params=params)
                # print(response.text)  # This will print the HTML content of the page

                # To mimic human-like intervals between requests
                time.sleep(15)  # Sleep for 15 seconds before making another request or closing the session

            except requests.exceptions.RequestException as e:
                response = ""
                print("Request failed: ", e)
        if response:
            print("Got Response From " + self.url + " " + query)
        
        soup = BeautifulSoup(response.content, "html.parser")

        return soup
    """