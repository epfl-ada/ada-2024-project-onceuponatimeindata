import os
import random

import numpy as np
import pandas as pd
import requests
import sys
import json

from tqdm import tqdm
from tqdm.contrib import itertools

current_dir = os.path.abspath("")
sys.path.append(current_dir)

from src.utils.general_utils import mkdir_no_exist

def get_data(keyword, end_date, keyword_id, start_date = "1880-01-01"):

    """
    Function to get data from TMDB API and save it as a CSV file.

    Parameters:
    -----------
    keyword: string
        Keyword to search for in the TMDB database.
    date: string
        Date to search for movies released before format : "YYYY-MM-DD".
    keyword_id: int
        Keyword id to search for in the TMDB database.
    start_date: string
        Date to search for movies released after format : "YYYY-MM-DD".
    """

    #
    api_key = open("api_key.txt", "r").read()


    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={end_date}&primary_release_date.gte={start_date}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    keyword = keyword.replace(" ", "_")
    total_page = get_total_page(headers, url)

    data_path = os.path.join(current_dir, "data", keyword)
    mkdir_no_exist(data_path)

    keyword = keyword + f"_{start_date[:4]}_{end_date[:4]}"
    csv_file = os.path.join(data_path, f"movie_with_{keyword}.csv")
    df = pd.DataFrame(columns=["id", "release_date", "original_title",  "title"])

    for page in tqdm(range(1, total_page + 1)):
        page_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={end_date}"
        df = df._append(get_movie_df(page_url, headers), ignore_index=True)
        df.to_csv(csv_file, index=False)

    with open(csv_file, "w") as f:
        df.to_csv(f, index=False)

    return df

def get_movie_df(page_url, headers):
    response = requests.get(page_url, headers=headers)
    data = response.json()
    df = pd.DataFrame(columns=["id", "release_date", "original_title", "title"])
    # addition of the movies to the dictionary with the id as the key
    for movie in data["results"]:
        movie_data = {"id": movie["id"],
                      'release_date': movie["release_date"],
                      "original_title": movie["original_title"],
                      "title": movie["title"]}
        df = df._append(movie_data, ignore_index=True)

    return df

def fill_missing_value(movie_entry, extended_dd_entry, replace_column, ref_column):
    if len(extended_dd_entry[ref_column]) == 0:
        return movie_entry
    if pd.isnull(movie_entry[replace_column]):
        movie_entry[replace_column] = extended_dd_entry[ref_column].values[0]
    return movie_entry

def get_movie_metadatalike_db(df, keyword, file_name=None):
    """
    Function to get data from TMDB API and save it as a CSV file. Use with database from get_movie_data_extended
    Writes in data/keyword/file_name_metadata.csv the component
    1. TMDB ID
    2. Movie name
    3. Movie release date
    4. Movie box office revenue
    5. Movie runtime
    6. Movie languages
    7. Movie countries
    8. Movie genres

    Parameters:
    -----------
    df: pandas dataframe containing the movies tmdb ids
    keyword: string
        Keyword to search for in the TMDB database.
    file_name: string
        Name of the file to save the data in.

    """


    if not file_name:
        file_name = keyword + "_metadata"

    data_path = os.path.join(current_dir, "data", keyword)
    mkdir_no_exist(data_path)
    csv_file = os.path.join(data_path, f"{file_name}.csv")

    df_out = pd.DataFrame()

    df_out["id"] = df["id"]
    df_out["Movie name"] = df["title"]
    df_out["Movie release date"] = df["release_date"]
    df_out["Movie box office revenue"] = df["revenue"]
    df_out["Movie runtime"] = df["runtime"]
    df_out["Movie languages"] = df["spoken_languages"]
    df_out["Movie countries"] = df["production_countries"]
    df_out["Movie genres"] = df["genres"]

    df_out.to_csv(csv_file, index=False)

    return df_out


def get_movie_data_extended(df, folder, file_name=None, year = ""):
    """
    Function to get data from TMDB API and save it as a CSV file.

    Parameters:
    -----------
    df: pandas dataframe containing the movies tmdb ids
    keyword: string
        Keyword to search for in the TMDB database.
    """

    if not file_name:
        file_name = folder + "_extended_" + year

    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    data_path = os.path.join(current_dir, "data", folder)
    mkdir_no_exist(data_path)
    csv_file = os.path.join(data_path, f"{file_name}.csv")

    df_out = None

    for key in tqdm(df["id"]):
        url = f"https://api.themoviedb.org/3/movie/{key}"
        response = requests.get(url, headers=headers)
        movie = response.json()
        movie_data = {
            "id" : movie["id"],
            'release_date' : movie["release_date"],
            "original_title" : movie["original_title"],
            "title" : movie["title"],
            "budget" : movie["budget"],
            "revenue" : movie["revenue"],
            "runtime" : movie["runtime"],
            "popularity" : movie["popularity"],
            "vote_average" : movie["vote_average"],
            "vote_count" : movie["vote_count"],
            "adult" : movie["adult"],
            "belongs_to_collection" : movie["belongs_to_collection"],
            "genres" : movie["genres"],
            "production_companies" : movie["production_companies"],
            "spoken_languages" : movie["spoken_languages"],
            "status" : movie["status"],
            "tagline" : movie["tagline"],
            "overview" : movie["overview"],
            "imdb_id" : movie["imdb_id"],
            "production_countries" : movie["production_countries"],
            "original_language" : movie["original_language"],
                      }

        if df_out is None:
            df_out = pd.DataFrame(columns=list(movie_data.keys()))
        df_out = df_out._append(movie_data, ignore_index=True)
        df_out.to_csv(csv_file, index=False)

    df_out.to_csv(csv_file, index=False)
    return df_out


def get_total_page(headers, url):
    response = requests.get(url, headers=headers)
    return response.json()["total_pages"]


def get_collection(panda_df, path="data", years="1880_2010"):
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


    if(not os.path.exists(os.path.join(path, f"collection_ids_{years}.json"))):
        for key in tqdm(panda_df["id"]):
            url = f"https://api.themoviedb.org/3/movie/{key}?append_to_response=changes"
            response = requests.get(url, headers=headers)
            if(response.json()["belongs_to_collection"]!= None):
                collection_id = response.json()["belongs_to_collection"]["id"]
                collection_set.add(collection_id)

        with open(os.path.join(path, f"collection_ids_{years}.json"), "w") as f:
            json.dump(list(collection_set), f)

    else:
        with open(os.path.join(path, f"collection_ids_{years}.json"), "r") as f:
            collection_set = set(json.load(f))


    df = pd.DataFrame(columns=["id", "release_date", "original_title",  "title"])
    df_extended = None
    collection_file = os.path.join(path, f"sequels_{years}.csv")
    collection_extended_file = os.path.join(path, f"sequels_extended_{years}.csv")

    for collection_id in tqdm(collection_set):
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

            url = f"https://api.themoviedb.org/3/movie/{movie['id']}"
            response = requests.get(url, headers=headers)
            movie_detailed = response.json()
            movie_data_extended = {
                "id" : movie_detailed["id"],
                'release_date' : movie_detailed["release_date"],
                "original_title" : movie_detailed["original_title"],
                "title" : movie_detailed["title"],
                "collection" : collection_name,
                "collection_id" : collection_id,
                "budget" : movie_detailed["budget"],
                "revenue" : movie_detailed["revenue"],
                "runtime" : movie_detailed["runtime"],
                "popularity" : movie_detailed["popularity"],
                "vote_average" : movie_detailed["vote_average"],
                "vote_count" : movie_detailed["vote_count"],
                "adult" : movie_detailed["adult"],
                "belongs_to_collection" : movie_detailed["belongs_to_collection"],
                "genres" : movie_detailed["genres"],
                "production_companies" : movie_detailed["production_companies"],
                "spoken_languages" : movie_detailed["spoken_languages"],
                "status" : movie_detailed["status"],
                "tagline" : movie_detailed["tagline"],
                "overview" : movie_detailed["overview"],
                "imdb_id" : movie_detailed["imdb_id"],
                "production_countries" : movie_detailed["production_countries"],
                "original_language" : movie_detailed["original_language"],
            }

            df = df._append(movie_data, ignore_index=True)

            if df_extended is None:
                df_extended = pd.DataFrame(columns=list(movie_data_extended.keys()))
            df_extended = df_extended._append(movie_data_extended, ignore_index=True)

    with open(collection_file, "w") as f:
        df.to_csv(f, index=False)

    df_extended.to_csv(collection_extended_file, index=False)
    return df, df_extended


import time


def get_wikipedia_id_from_title(title, date):
    api_key = open("api_wiki_key.txt", "r").read()

    headers = {
        'Authorization': 'Bearer ' + api_key
    }

    year = str(date)[:4] if date else ""
    title += " film, " + (str(year) if str.isdigit(year) else "")
    title.replace(" ", "%20")

    language_code = 'en'
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': title, 'limit': 1}
    response = requests.get(url, headers=headers, params=parameters)
    while response.status_code != 200:
        print(response.status_code)
        time.sleep(60)
    page = requests.get(url, headers=headers, params=parameters).json().get('pages')
    id = page[0].get('id', 0) if page else 0
    id = int(id) if id else None
    return id

def randomly_sample_movie(start_date, end_date, sample_size, num_vote=10):
    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    urls = []
    num_page_per_year = []
    for i in range (start_year, end_year):
        start_date_year_str = str(i) + "-01-01"
        end_date_year_str = str(i + 1) + "-01-01"

        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=title.asc&primary_release_date.lte={end_date_year_str}&primary_release_date.gte={start_date_year_str}&vote_count.gte={num_vote}"

        response = requests.get(url, headers=headers)
        number_of_pages = response.json()["total_pages"]

        urls.append(url)
        num_page_per_year.append(number_of_pages)
    p = np.array(num_page_per_year) / np.sum(num_page_per_year)
    movie_per_page = 20
    num_sample_per_year = (np.array([sample_size for x in range(len(num_page_per_year))]) * p / movie_per_page).astype(int)

    df = None
    for i in tqdm(range(end_year - start_year)):
        pages_sampled = np.random.choice(range(1, num_page_per_year[i]), num_sample_per_year[i])
        for p in pages_sampled:
            url_page = urls[i].replace("page=1", f"page={p}")
            movie_df = get_movie_df(url_page, headers)
            if(df is None):
                df = pd.DataFrame(columns=list(movie_df.columns))
            df = df._append(movie_df, ignore_index=True)

    df.to_csv(f"data/random_sample/random_sample_{start_year}_{end_year}.csv", index=False)
    get_movie_data_extended(df, "random_sample", f"random_sample_{start_year}_{end_year}_extended")
    get_movie_metadatalike_db(df, "random_sample", f"random_sample_{start_year}_{end_year}_metadata")

    return df




def json_to_csv(input_file, output_file):
    import pandas as pd
    with open(input_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)