import requests
from bs4 import BeautifulSoup
from web_scraper import FACULTY_LISTING_SCRAPER

class UMD_SCRAPER(FACULTY_LISTING_SCRAPER):
    def __init__(self, url: str):
        self.url = url
    
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    def clean_up(self, html_element):
        soup = BeautifulSoup(str(html_element), 'html.parser')

        # sample tag below, only applicable for umd staff directory:
        # <a id="undefined" name="undefined" style="color: black;">Abadi</a>

        # Find the <a> tag and get its text content
        name_tag = soup.find('a')  # Since there's only one <a> tag in this snippet
        name = name_tag.get_text() if name_tag else 'No name found'
        return str(name)

    def extract_profs_information(self):
        toRet = []
        soup = self.get_soup()

        # first name list includes middle name
        profs_first_names = soup.select("table.faculty tbody tr td:nth-of-type(2)")
        profs_last_names = soup.select("table.faculty tbody tr td:first-of-type")
        profs_majors = soup.select("table.faculty tbody tr td:nth-of-type(5)")


        for i in range(len(profs_first_names)):
            prof_first_name = profs_first_names[i]
            profs_last_name = profs_last_names[i]
            prof_major = profs_majors[i]


            if prof_first_name.contents and profs_last_name.contents and prof_major.contents:
                first, last = str(prof_first_name.contents[0]), str(profs_last_name.contents[0])
                new_first, new_last = "", ""
                if not "id" in str(first) and not "id" in str(last):
                    toRet.append((first, last))
                elif "id" in str(first):
                    new_first = self.clean_up(first)
                    first = ""
                elif "id" in str(last):
                    new_last = self.clean_up(last)
                    last = ""

                majors = [major for major in prof_major.contents if major != "<br/>"]
                
                toRet.append({"name": (first + new_first, last + new_last), "majors":majors})

        return toRet
    
