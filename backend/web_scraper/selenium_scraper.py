from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get("https://scholar.google.com/citations?user=rcnh2c4AAAAJ&hl=en")
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all 'a' tags (links) in the parsed HTML
    links = soup.find_all('a')

    pattern = re.compile(r'^/citations\?view_op=view_citation&hl=en&user=.+&citation_for_view=.+$')

    # Extract the links that match the pattern
    matching_links = ["https://scholar.google.com" + link.get('href') for link in links if pattern.match(link.get('href', ''))]
    
    print("-"*50)
    # Print all the links found
    for link in matching_links:
        print(link)
        driver.get(link)
        # try:
        #     abstract = driver.find_element(By.CLASS_NAME, 'gsh_csp')
        # except:
        #     abstract = driver.find_element(By.CLASS_NAME, 'gsh_small')
        # print(abstract.text)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find('meta', property='og:title')['content']
        print(title)
    print("-"*50)
    
    driver.quit()

if __name__ == "__main__":
    main()