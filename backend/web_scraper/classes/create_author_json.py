from author import AUTHOR
from sentence_transformers import SentenceTransformer
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import json

def embed_abstracts(abstracts_list):
    # taking the mean of each column and making that the element of each row (to flatten matrix)

    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings_mat = [model.encode([embeddingString])[0] for embeddingString in abstracts_list]
    vector = np.mean(embeddings_mat, axis=0)
    return vector.tolist()

def get_abstracts_from_author_page(author_page_link):
    abstracts = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(author_page_link)
        
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
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                abstract = driver.find_element(By.CLASS_NAME, 'gsh_csp')
                title = soup.find('meta', property='og:title')['content']
                abstracts.append(title + ":\n" + abstract.text)
            except Exception as e:
                print("Error with using element gsh_csp:")
            try:
                abstract = driver.find_element(By.CLASS_NAME, 'gsh_small')
                title = soup.find('meta', property='og:title')['content']
                abstracts.append(title + ":\n" + abstract.text)
            except Exception as e:
                print("Error with using element gsh_small:")
                abstracts.append("")
        print("-"*50)
        
        driver.quit()
    except Exception as e:
        print("Could not get abstract")
        print(e)

    return abstracts


def create_vector_data_file(all_info):
    vectors = []
    total = len(all_info)
    for i, info in enumerate(all_info):
        if i % 5 == 0:
            print("-"*50)
            print("Percent Done:", (i/total)*100)
            print("-"*50)
        metadata = {}

        for key in info:
            metadata[key] = info[key]

        author = info["Name"]
        author_obj = AUTHOR(author_name=author)

        print("Author:", author)

        profile_page = author_obj.get_profile_page()

        print("Profile Page:", profile_page)

        abstracts = get_abstracts_from_author_page(profile_page)
        print("ABSTRACTS")
        print("-"*50)
        for a in abstracts:
            if a:
                print("-"*50)
                print(a)
                print("-"*50)
        print("-"*50)
        metadata["abstracts"] = abstracts
        embedding = embed_abstracts(abstracts)

        vectors.append({"id":i, "values":embedding, "metadata":metadata})

    with open('faculty_data/umd_data_to_insert.json', 'w') as json_file:
        json.dump(vectors, json_file, indent=4)
        


def main():
    with open("faculty_data/umd_faculty_data.json") as file:
        umd_faculty_data = json.load(file)
    
    create_vector_data_file(umd_faculty_data)

if __name__ == "__main__":
    main()
        