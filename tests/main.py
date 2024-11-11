import fuzzymatcher
import pandas as pd
import difflib

import requests

import swifter
from tqdm import tqdm
from fuzzywuzzy import process

from src.data.TMDB_Movies import get_data, get_collection


def get_wikidata_id_from_wikipedia_id(wikipedia_id):
    """
    Get the wikidata id from the wikipedia id.

    Parameters:
    wikipedia_id: str
        The wikipedia id of the movie.
    """
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&pageids={wikipedia_id}"
    response = requests.get(url)
    wikidata_id = response.json().get('query', {}).get('pages', {}).get(str(wikipedia_id), {}).get('pageprops', {}).get(
        'wikibase_item')
    return wikidata_id


def get_wikidata_id_from_tmdb_id(tmdb_id):
    """
    Get the wikidata id from the tmdb id.

    Parameters:
    tmdb_id: str
        The tmdb id of the movie.
    """

    if not type(tmdb_id) is int:
        return None

    api_key = open("api_key.txt", "r").read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
    response = requests.get(url, headers=headers)
    wikidata_id = response.json().get('wikidata_id', {})
    return wikidata_id

if __name__ == "__main__":
    movie_df = pd.read_csv('data/MovieSummaries/movie.metadata.tsv', sep='\t', header=None)
    sequel_collections = pd.read_csv('data/collections/sequels.csv')


    pd.DataFrame.swifter.progress_bar(enable=True, desc=None)
    sequel_collections["wikidata movie ID"] = sequel_collections["id"].swifter.progress_bar(enable=False, desc=None).apply(
        get_wikidata_id_from_tmdb_id)



