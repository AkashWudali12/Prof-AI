import requests
import json
import pprint

# URL you want to make a GET request to

profiles_url = "https://serpapi.com/search?engine=google_scholar_profiles"

api_key =  "f2e136019dbe8daaab3095b82c3d9d1b68a3224f079edc6ee7aa23e2d1ca66a4"

params = {
  "api_key": api_key,
  "mauthors": "Eyad Abed",
}

# Make the GET request with query parameters
response = requests.get(profiles_url, params)

# Check the response
if response.status_code == 200:
    data = response.json()
    id = data["profiles"][0]["author_id"]
    print("Got Data")
    print(id)
else:
    print("Failed to retrieve data:", response.status_code)
    print("Message", response.json())

author_params = {
  "api_key": api_key,
  "author_id": id,
}

authors_url = "https://serpapi.com/search?engine=google_scholar_author"

response = requests.get(authors_url, author_params)

if response.status_code == 200:
    data = response.json()
    print("Got Data")
    print(response.json())
else:
    print("Failed to retrieve data:", response.status_code)
    print("Message", response.json())



# this output gives information about the incorrect professor

