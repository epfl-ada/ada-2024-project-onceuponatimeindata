import os
import time
from collections.abc import Set

import pandas as pd
import requests
import sys
import json

import tqdm
from IPython.core.completerlib import module_completer

current_dir = os.path.abspath("")
sys.path.append(current_dir)

from src.utils.general_utils import mkdir_no_exist

def get_data(keyword, date, keyword_id):

    """
    Function to get data from TMDB API and save it as a CSV file.

    Parameters:
    -----------
    keyword: string
        Keyword to search for in the TMDB database.
    date: string
        Date to search for movies released before format : "YYYY-MM-DD".
    """

    api_key = open("api_key.txt", "r").read()


    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={date}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    total_page = get_total_page(headers, url)

    data_path = os.path.join(current_dir, "data")
    csv_file = os.path.join(data_path, f"movie_with_keyword_{keyword}.csv")
    df = None

    for page in tqdm.tqdm(range(1, total_page + 1)):
        page_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={date}"
        response = requests.get(page_url, headers=headers)
        data = response.json()
        #addition of the movies to the dictionary with the id as the key
        for movie in data["results"]:
            movie_data = {"id" : movie["id"],
                'release_date' : movie["release_date"],
                "original_title" : movie["original_title"],
                "title" : movie["title"]}
            df = df._append(movie_data, ignore_index=True) if not df is None else pd.DataFrame([movie_data])

    with open(csv_file, "w") as f:
        df.to_csv(f, index=False)




def get_total_page(headers, url):
    response = requests.get(url, headers=headers)
    return response.json()["total_pages"]


def get_collection(panda_df):
    """
    writes the movies together in the same collection

    Parameters:

        panda_df: pandas dataframe containing the movies ids
    """

    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    collection_set = set()


    collection_path = os.path.join(current_dir, "data", "collections")
    mkdir_no_exist(collection_path)

    if(not os.path.exists(os.path.join(collection_path, "collection_ids.json"))):
        for key in tqdm.tqdm(panda_df["id"]):
            url = f"https://api.themoviedb.org/3/movie/{key}?append_to_response=changes"
            response = requests.get(url, headers=headers)
            if(response.json()["belongs_to_collection"]!= None):
                collection_id = response.json()["belongs_to_collection"]["id"]
                collection_set.add(collection_id)

        with open(os.path.join(collection_path, "collection_ids.json"), "w") as f:
            json.dump(list(collection_set), f)

    else:
        with open(os.path.join(collection_path, "collection_ids.json"), "r") as f:
            collection_set = set(json.load(f))


    df = None
    collection_file = os.path.join(collection_path, f"sequels.csv")

    for collection_id in tqdm.tqdm(collection_set):
        url = f"https://api.themoviedb.org/3/collection/{collection_id}"
        response = requests.get(url, headers=headers)
        collection = response.json()
        collection_name = collection["name"]
        skip = False
        for movie in collection["parts"]:
            if (movie["adult"] == True):
                skip = True
        if skip:
            continue

        for movie in collection["parts"]:
            movie_data = {"id" : movie["id"],
                'release_date' : movie["release_date"],
                "original_title" : movie["original_title"],
                "title" : movie["title"],
                "collection" : collection_name,
                "collection_id" : collection_id}
            if(movie["adult"] == True):
                skip = True
            df = df._append(movie_data, ignore_index=True) if not df is None else pd.DataFrame([movie_data])

    with open(collection_file, "w") as f:
        df.to_csv(f, index=False)





def json_to_csv(input_file, output_file):
    import pandas as pd
    with open(input_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)