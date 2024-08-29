from scholarly import scholarly
from pprint import pprint

class AUTHOR_FINDER:
    def __init__(self):
        pass
    def get_papers(self, keywords):
        search_query = scholarly.search_keyword(keywords)
        # list of dictionaries, use the "name" key to get author names
        return search_query
    def find_best_authors(self, num_authors, papers):
        author_names = []
        i = 0
        for paper_info in papers:
            if i < num_authors:
                if "name" in paper_info:
                    author_names.append(paper_info["name"])
            else:
                break
            i += 1
        return author_names


