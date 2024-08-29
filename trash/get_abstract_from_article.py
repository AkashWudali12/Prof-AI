from scholarly import scholarly
from pprint import pprint

class ABSTRACT_EXTRACTOR:
    def __init__(self):
        pass
    def get_abstract(self, article_author, article_title):
        count = 0
        abstract_content = ""
        try:
            search_query = scholarly.search_pubs(article_title)
            print(search_query)
            print("Got results")
            for pub in search_query:
                print(pub)
                author_first_last_list = article_author.split(" ")
                if len(author_first_last_list) == 2:
                    author_last_name = author_first_last_list[1]
                else:
                    author_last_name = "NONE"
                if author_last_name in " ".join(pub["bib"]["author"]):
                    abstract_content = pub["bib"]["abstract"]
                    break
                if count == 10:
                    break
                count += 1
                return abstract_content
        except:
            print("Could not retrieve abstract")
            return ""
            