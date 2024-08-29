import requests
from bs4 import BeautifulSoup
from classes.id_scraper import ID_SCRAPER
from classes.author_scraper import AUTHOR_SCRAPER

class RESEARCH_PAPER_FINDER:
    def __init__(self, author_name):
        self.name = author_name
        self.id_scraper = ID_SCRAPER(author_name)
        self.id = self.id_scraper.get_id()

        self.author_serp_scraper = AUTHOR_SCRAPER(self.id)
        self.links = self.author_serp_scraper.get_article_links()

    def get_papers(self):
        for link in self.links:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")
            print(soup)
            break
