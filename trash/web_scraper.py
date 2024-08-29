import requests
from bs4 import BeautifulSoup


class FACULTY_LISTING_SCRAPER:
    def __init__(self, url: str):
        raise NotImplementedError("Constructor must be implemented")
    def get_first_and_last_names(self) -> list:
        raise NotImplementedError("Method get_first_and_last_names must be implemented")
    
    

"""
def crawl_search(init_url):
    # performs a BFS of each of the links and their sublinks related to the root (init_url)

    # initialize the list of discovered urls
    # with the first page to visit
    urls = [init_url]

    ct = 0
    
    # until all pages have been visited
    while len(urls) != 0:
        # get the page to visit from the list
        current_url = urls.pop()
        ct += 1
        
        # crawling logic
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, "html.parser")
    
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            if init_url in url:
                urls.append(url)
    
    # as a test return the count
    return ct


---------- Notes --------------- 

# return bs4 set of all the html contents with a specific tag and element
# in this case, because I want link I passed "a[href]" which are the elements with links
link_elements = soup.select("a[href]")


# can search individual link_element (which has a specified tag) like a dictionary to look for href element
urls = []
for link_element in link_elements:
   url = link_element['href']
   if "https://www.scrapingcourse.com/ecommerce/" in url:
      urls.append(url)

-------------------------------- 

"""