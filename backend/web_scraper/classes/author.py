import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import json
from googleapiclient.discovery import build
from human_request import HUMAN_REQUEST
import re
from bs4 import BeautifulSoup
import time



# URL you want to make a GET request to

load_dotenv("my_env.env")
api_key = "AIzaSyB24OqS9PIVha49xvHGb6IvlsN2t56LBEE"
search_engine_id = "e6a0456e3f63b45e5"
regular_google_search_id = "570a8aec146c54b05"


class AUTHOR:
    def __init__(self, author_name):
        self.author_name = author_name
        self.page_link = ""
    
    def make_request_to_google(self, query):
        payload = {
            'key':api_key,
            'q':query,
            'cx':search_engine_id,
            'start':1,
            'num':10
        }

        print("Query:", query)

        response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)

        if response.status_code == 200:
            print("Request Successful")
            return response.json()
        else:
            print("Could not get author's information")
            print(response.json())
            return ""
            
    def get_profile_page(self):
        try:
            data = self.make_request_to_google(self.author_name)
            time.sleep(5)
            self.page_link = data["items"][0]["link"]
            return self.page_link
        except:
            print("Could not get author's information link")
            return ""
    
    def get_abstracts(self):
        self.article_links = []
        self.articles_info = []
        self.titles_links = []
        try:
            human_request = HUMAN_REQUEST(self.page_link)
            soup = human_request.get_soup()

            print("Soup Text:", soup.text)

            ## add option to see if soup is
            article_titles = [itm.get_text() for itm in soup.find_all('a', class_='gsc_a_at')]

            # print("article titles:", article_titles)

            # Find all the links
            links = soup.find_all('a')

            pattern = re.compile(r'^/citations\?view_op=view_citation&hl=en&user=.+&citation_for_view=.+$')

            # Extract the links that match the pattern
            matching_links = ["https://scholar.google.com" + link.get('href') for link in links if pattern.match(link.get('href', ''))]

            # print("article_links:", matching_links)

            self.titles_links = list(zip(article_titles, matching_links))
        except Exception as e:
            print("Could not get any article links")
            print(e)
            return self.articles_info
        
        # print(self.titles_links)

        for itm in self.titles_links:
            print("-"*100)
            try:
                article_title, article_url = itm

                time.sleep(5)

                human_request_abstract = HUMAN_REQUEST(url=article_url)
            
                abstract_soup = human_request_abstract.get_soup()

                description = abstract_soup.find('meta', property='og:description')['content']
                abstract = abstract_soup.select_one('div#gsc_oci_descr .gsh_csp').text

                article_info = {
                    "article_title": article_title,
                    "description": description,
                    "article_url": article_url,
                    "article_abstract":abstract
                }

                # for key, value in article_info.items():
                #     print(f"{key}: {value}")

                self.articles_info.append(article_info)

                print("Got Info")
            except Exception as e:
                print(e)
                print("Could not get article information")
            print("-"*100)
        
        print("Got Articles Info")
        return self.articles_info

    
    def get_author_picture(self, file_path):
        try:
            human_request = HUMAN_REQUEST(self.page_link)
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

