import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from human_request import HUMAN_REQUEST

# URL you want to make a GET request to

load_dotenv("my_env.env")
api_key = os.environ.get("SERP_API_KEY")

class ID_SCRAPER:
    def __init__(self, author_name):
        self.author_name = author_name
        self.response = ""
    
    def request(self):
        profiles_url = "https://serpapi.com/search?engine=google_scholar_profiles"

        params = {
        "api_key": api_key,
        "mauthors": self.author_name,
        }

        response = requests.get(profiles_url, params)

        return response
    
    def get_id(self):
        if not self.response:
            self.response = self.request()
        
        if self.response.status_code == 200:
            data = self.response.json()
            a_id = data["profiles"][0]["author_id"]
        else:
            print("Failed to retrieve data:", self.response.status_code)
            print("Message", self.response.json())
            a_id = None
        return a_id
    
    def get_author_page(self):
        if not self.response:
            self.response = self.request()
        
        if self.response.status_code == 200:
            data = self.response.json()
            author_page_url = None
            count = 0
            if "profiles" in data:
                count += 1
                author_page_url = data["profiles"]
            if author_page_url:
                count += 1
                author_page_url = author_page_url[0]
            if "link" in author_page_url:
                count += 1
                author_page_url = author_page_url["link"]
            if count == 3:
                return author_page_url
            else:
                print("Could not retrieve link from request")
                return None
        else:
            print("Failed to retrieve data:", self.response.status_code)
            print("Message", self.response.json())
            return None
    
    def get_author_picture(self, file_path):
        try:
            author_page_url = self.get_author_page()
            print(author_page_url)
            human_request = HUMAN_REQUEST(author_page_url)
            soup = human_request.get_soup()
            og_image_meta = soup.find('meta', property="og:image")
            image_url = og_image_meta['content']
            human_img_request = HUMAN_REQUEST(image_url)
            img_response = human_img_request.get_response()
            
            if img_response.status_code == 200:
                # Open a file to write the binary stream
                with open(file_path + '.jpg', 'wb') as file:
                    file.write(img_response.content)
                print("Image downloaded successfully.")
            else:
                print("Failed to retrieve image.")
        except:
            print("Failed to retrieve image.")



        
    