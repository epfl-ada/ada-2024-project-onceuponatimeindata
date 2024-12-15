import os
from concurrent.futures import ThreadPoolExecutor

from fuzzywuzzy.fuzz import ratio
import numpy as np
import pandas as pd
import requests
import sys
import json

from more_itertools import sliced
from tqdm import tqdm

current_dir = os.path.abspath("")
sys.path.append(current_dir)

from src.utils.general_utils import mkdir_no_exist

def get_data(keyword, start_date, end_date, keyword_id, file_path):

    """
    Function to get data from TMDB API and save it as a CSV file.

    :param keyword: string
        Keyword to search for in the TMDB database.
    :param start_date: string
        Date to search for movies released after format : "YYYY-MM-DD".
    :param end_date: string
        Date to search for movies released before format : "YYYY-MM-DD".
    :param keyword_id: int
        Keyword id to search for in the TMDB database.
    :param file_path: string
        Path to save the CSV file.
    """
    api_key = open("api_key.txt", "r").read()


    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={end_date}&primary_release_date.gte={start_date}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    total_page = get_total_page(headers, url)


    keyword = keyword
    csv_file = file_path
    df = pd.DataFrame(columns=["id", "release_date", "original_title",  "title"])
    dict = {}

    for page in tqdm(range(1, total_page + 1), desc=f"Getting {keyword} movies"):
        page_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&with_keywords={keyword_id}&primary_release_date.lte={end_date}&primary_release_date.gte={start_date}"
        movies_df = get_movie_df(page_url, headers)
        for key in movies_df["id"]:
            dict[key] = movies_df[movies_df["id"] == key].to_dict(orient='records')[0]

    df = pd.DataFrame.from_dict(dict, orient='index')
    df.to_csv(csv_file, index=False)

    return df

def get_movie_df(page_url, headers):
    """
    Fetches movie data from a given TMDB API page URL and returns it as a pandas DataFrame.

    :param page_url: str
        The URL of the TMDB API page to fetch movie data from.
    :param headers: dict
        The headers to include in the API request.
    :return: pandas.DataFrame
        A DataFrame containing movie data with columns: id, release_date, original_title, title.
    """
    response = requests.get(page_url, headers=headers)
    data = response.json()
    df = pd.DataFrame(columns=["id", "release_date", "original_title", "title"])
    dict = {}
    # addition of the movies to the dictionary with the id as the key
    if "results" not in data:
        return df
    for movie in data["results"]:
        if "id" not in movie:
            continue
        movie_data = {"id": movie.get("id", -1),
                      'release_date': movie.get("release_date", ""),
                      "original_title": movie.get("original_title", ""),
                      "title": movie.get("title", "")}
        dict[movie["id"]] = movie_data

    df = pd.DataFrame.from_dict(dict, orient='index')
    return df

def fill_missing_value(movie_entry, extended_dd_entry, replace_column, ref_column):
    """
    Fill missing values in the movie entry with values from the extended data entry.

    :param movie_entry: pandas.Series
        The movie entry from the main DataFrame.
    :param extended_dd_entry: pandas.DataFrame
        The extended data entry containing additional information.
    :param replace_column: str
        The column name in the movie entry to be filled.
    :param ref_column: str
        The reference column name in the extended data entry to get the value from.
    :return: pandas.Series
        The updated movie entry with filled values.
    """
    if len(extended_dd_entry[ref_column]) == 0:
        return movie_entry
    if pd.isnull(movie_entry[replace_column]):
        movie_entry[replace_column] = extended_dd_entry[ref_column].values[0]
    return movie_entry

def get_movie_metadatalike_db(df, file_path):
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

    :param df: pandas dataframe
        Dataframe containing the movies data.
    :param file_path: string
        Path to save the CSV file.

    """

    csv_file = file_path

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
    assert (pd.read_csv(csv_file).shape[0] == df.shape[0])

    return df_out


def get_movie_data_extended(df, file_path):
    """
    Function to get data from TMDB API and save it as a CSV file. Use with database from get_data
    :param df: dataframe containing the movies data
    :param file_path: path to file
    :return: dataframe containing the movies data extended
    """

    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    csv_file = file_path

    i = 0
    dict = {}
    def process_movie_data(key):
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
        return key, movie_data

    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_movie_data, df["id"]), total=len(df["id"]), desc="Getting movie data extended"))

    dict = {key: movie_data for key, movie_data in results}

    df_out = pd.DataFrame.from_dict(dict, orient='index')
    df_out.to_csv(csv_file, index=False)
    return df_out


def get_total_page(headers, url):
    response = requests.get(url, headers=headers)
    return response.json()["total_pages"]


def get_collection(panda_df, path="data", years="1880_2010"):
    """
    Function to get the collection of movies from the TMDB API and save it as a CSV file.
    :param panda_df: dataframe containing the sequel movies data
    :param path: path to save the CSV file
    :param years: release date of the movies
    :return: dataframe containing the collection of movies
    """

    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    collection_set = set()


    if(not os.path.exists(os.path.join(path, f"collection_ids_{years}.json"))):
        for key in tqdm(panda_df["id"], desc="Getting collection ids"):
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


    dict = {}
    dict_extended = {}
    collection_file = os.path.join(path, f"sequels_and_original_{years}.csv")
    collection_extended_file = os.path.join(path, f"sequels_and_original_{years}_extended.csv")
    collection_metadata_file = os.path.join(path, f"sequels_and_original_{years}_metadata.csv")

    for collection_id in tqdm(collection_set, desc="Retrieving collections"):
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


            dict[movie["id"]] = movie_data
            dict_extended[movie["id"]] = movie_data_extended

    df = pd.DataFrame.from_dict(dict, orient='index')
    df_extended = pd.DataFrame.from_dict(dict_extended, orient='index')

    df_metadata = get_movie_metadatalike_db(df_extended, collection_metadata_file)

    df.to_csv(collection_file, index=False)
    df_extended.to_csv(collection_extended_file, index=False)

    assert (pd.read_csv(collection_file).shape[0] == df.shape[0])
    assert (pd.read_csv(collection_extended_file).shape[0] == df_extended.shape[0])
    return df, df_extended


import time


def get_wikipedia_id_for_db(df, file):
    """
    Function to get the wikipedia id for the movies in the dataframe and save it as a CSV file.
    :param df: dataframe containing the movies data
    :param file: file to be saved to
    :return: dataframe containing the wikipedia id for the movies
    """
    wiki_df = None
    wiki_df = pd.read_csv(file) if os.path.exists(file) else wiki_df
    df_null = wiki_df[wiki_df["Wikipedia movie ID"] == -1] if wiki_df is not None else df
    wiki_df = wiki_df[wiki_df["Wikipedia movie ID"] != -1] if wiki_df is not None else None
    df_not_in_wiki = df[~df["id"].isin(wiki_df["id"])] if wiki_df is not None else df

    df_null = pd.concat([df_null, df_not_in_wiki])

    #split the dataframe into chunks 1000 long, wikipedia API limit is 5000
    split_df = np.array_split(df_null, len(df_null) //1000 + 1)

    for part_df in split_df:

        slices = sliced(seq=range(len(part_df)), n=50)

        def process_chunk(index):
            chunk = part_df.iloc[index].copy()
            chunk["Wikipedia movie ID"] = chunk.apply(lambda x: get_wikipedia_id_from_title(x["title"], x["release_date"]),
                                                      axis=1)
            return chunk

        with ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(process_chunk, slices), total=len(part_df) // 50, desc="Getting wikipedia id"))

        for chunk in results:
            if wiki_df is None:
                wiki_df = chunk
            else:
                wiki_df = pd.concat([wiki_df, chunk])

        wiki_df.to_csv(file)
        assert (pd.read_csv(file).shape[0] == wiki_df.shape[0])
    return wiki_df

def get_wikipedia_id_from_title(title, date):
    """
    Function to get the wikipedia id for a movie title. Researches wikipedia for the movie title + year and returns the id.
    :param title: Title of the movie
    :param date: release date of the movie
    :return: id of movie in wikipedia
    """
    api_key = open("api_wiki_key.txt", "r").read()

    headers = {
        'Authorization': 'Bearer ' + api_key
    }

    year = str(date)[:4] if date else ""
    year = year if str.isdigit(year) else ""
    title_request = title + f" film {year}"
    title_request.replace(" ", "+")

    language_code = 'en'
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': title_request, 'limit': 5}
    response = requests.get(url, headers=headers, params=parameters)
    i = 0
    while response.status_code != 200:
        print(response.status_code, end="\r")
        print(f"title : {title}", end="\r")
        #response = requests.get(url, headers=headers, params=parameters)
        return -1
    page = response.json().get('pages')
    best_ratio = 0
    best_id = -1
    word_found = False
    for p in page:
        page_title = p.get('title', "")

        if p.get('description', "") and "film" in p.get('description', "") and year in p.get('description', ""):
            best_id = p.get('id', -1)
            word_found = True

        if ratio(page_title, title + f" (film)") > 98 or ratio(page_title, title + f" ({year} film)") > 98:
            best_id = p.get('id', -1)
            return best_id

        r = ratio(p.get('title', ""), title)
        if r > best_ratio:
            if word_found and p.get('description', "") and "film" in p.get('description', "") and year in p.get('description', ""):
                best_ratio = r
                best_id = p.get('id', -1)
                continue
            if word_found:
                continue
            best_ratio = r
            best_id = p.get('id', -1)
    return best_id

def randomly_sample_movie(start_date, end_date, sample_size, file_path, num_vote=10):
    """
    Used to randomly sample movies from the TMDB API, to create a baseline comparaison
    :param start_date: start date of the movies sampled
    :param end_date: end date of the movies sampled
    :param sample_size: number of movies sampled
    :param file_path: path to save the CSV file
    :param num_vote: minimum number of votes for the movie to be considered
    :return: the dataframe containing the sampled movies
    """

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

    dict = {}
    for i in tqdm(range(end_year - start_year), desc="Getting random sample"):
        pages_sampled = np.random.choice(range(1, num_page_per_year[i]), num_sample_per_year[i])
        for p in pages_sampled:
            url_page = urls[i].replace("page=1", f"page={p}")
            movie_df = get_movie_df(url_page, headers)
            for key in movie_df["id"]:
                dict[key] = movie_df[movie_df["id"] == key].to_dict(orient='records')[0]

    df = pd.DataFrame.from_dict(dict, orient='index')
    df.to_csv(f"data/random_sample/random_sample_{start_year}_{end_year}.csv", index=False)
    assert (pd.read_csv(f"data/random_sample/random_sample_{start_year}_{end_year}.csv").shape[0] == df.shape[0])
    df_ext = get_movie_data_extended(df,  f"data/random_sample/random_sample_{start_year}_{end_year}_extended.csv")
    get_movie_metadatalike_db(df_ext, f"data/random_sample/random_sample_{start_year}_{end_year}_metadata")

    return df

def sample_all_movie(start_date, end_date, file_path, num_vote=10):
    """
    Used to sample all movies from the TMDB API, to create a baseline comparaison
    :param start_date: start date of the movies sampled
    :param end_date: end date of the movies sampled
    :param file_path: path to save the CSV file
    :param num_vote: minimum number of votes for the movie to be considered
    """
    api_key = open("api_key.txt", "r").read()

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    dict = {}
    for year in range(start_year, end_year):
        date = str(year) + "-01-01"
        next_date = str(year + 1) + "-01-01"
        url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&"
               f"language=en-US&page=1&sort_by=title.asc&primary_release_date.lte={next_date}"
               f"&primary_release_date.gte={date}&vote_count.gte={num_vote}")

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }

        total_page = get_total_page(headers, url)

        with ThreadPoolExecutor() as executor:
            def process_page(page):
                page_url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&"
                            f"language=en-US&page={page}&sort_by=title.asc&primary_release_date.lte={next_date}"
                            f"&primary_release_date.gte={date}&vote_count.gte={num_vote}")
                movies_df = get_movie_df(page_url, headers)
                return {key: movies_df[movies_df["id"] == key].to_dict(orient='records')[0] for key in movies_df["id"]}

            results = list(
                tqdm(executor.map(process_page, range(1, total_page + 1)), total=total_page, desc="Getting all movies"))
            for result in results:
                dict.update(result)

        df = pd.DataFrame.from_dict(dict, orient='index')
        df.to_csv(file_path, index=False)

    df = pd.DataFrame.from_dict(dict, orient='index')
    df.to_csv(file_path, index=False)
    assert (pd.read_csv(file_path).shape[0] == df.shape[0])
    df_ext = get_movie_data_extended(df, file_path.replace(".csv", "_extended.csv"))
    get_movie_metadatalike_db(df_ext, file_path.replace(".csv", "_metadata.csv"))








def json_to_csv(input_file, output_file):
    import pandas as pd
    with open(input_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)