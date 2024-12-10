import numpy as np
import pandas as pd
from tqdm import tqdm
from sympy.benchmarks.bench_discrete_log import data_set_1

from data.TMDB_Movies import get_data, get_movie_data_extended, get_movie_metadatalike_db, get_collection, \
    get_wikipedia_id_for_db, fill_missing_value, randomly_sample_movie
from utils.general_utils import mkdir_no_exist


def ensure_same_year(df):
    """
    Ensure that the release year from the wikipedia data and the tmdb data are the same
    :param df: dataframe with the wikipedia data. Must have the columns "Movie release date" and "release_date"
    :return: the dataframe with the release year columns
    """
    df["release year wiki"] = df["Movie release date"].apply(
        lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
    df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)

    df.drop(df[df["release year wiki"] != df["release year tmdb"]].index, inplace=True)
    df["release year"] = df["release year wiki"].astype(float)
    df.drop("release year tmdb", axis=1, inplace=True)
    df.drop("release year wiki", axis=1, inplace=True)

    return df

def get_movies(keywords_name, keywords_id, start_date, end_date):
    """
    Get the movies from the tmdb api and the wikipedia api
    :param keywords_name: The string name of the keywords
    :param keywords_id: The id of the keywords
    :param start_date: The start date of the movies format "YYYY-MM-DD"
    :param end_date: The end date of the movies format "YYYY-MM-DD"
    :return: None
    """
    years = f"{start_date[:4]}_{end_date[:4]}"

    datas, datas_extended, meta_data_likes = get_movies_from_tmdb(keywords_id, keywords_name, start_date, end_date)


    sequel_collections, _= get_collection(datas["sequels"], path="data/collections", years=years)

    sequel_collections_with_wiki_id = get_wikipedia_id_for_db(sequel_collections, f"data/collections/sequels_and_original_{years}_with_wiki_id.csv")
    wiki_id = {}
    datas = {"sequels": pd.read_csv('data/sequels/sequels_1880_2010.csv')}
    datas_extended = {"sequels": pd.read_csv('data/sequels/sequels_extended_1880_2010.csv')}
    for data, keyword_name in zip(datas.values(), datas.keys()):
        file_name = f"{keywords_name}_with_wiki_id_{start_date[:4]}_{end_date[:4]}.csv"

        wiki_id[keyword_name] = get_wikipedia_id_for_db(data, f"data/{keyword_name}/{file_name}")

    if int(end_date[:4]) <= 2010:
        movie_df = pd.read_csv('data/MovieSummaries/movie.metadata.tsv', sep='\t', header=None)
        movie_df.rename(columns={0: 'Wikipedia movie ID', 1: "Freebase movie ID", 2: "Movie name", 3: "Movie release date",
                                 4: "Movie box office revenue", 5: "Movie runtime", 6: "Movie languages",
                                 7: "Movie countries", 8: "Movie genres"}, inplace=True)
        movie_df_sequel_original = movie_df.join(sequel_collections_with_wiki_id.set_index('Wikipedia movie ID'),
                                                 on="Wikipedia movie ID", how='inner')
        movie_df_sequel_original.to_csv('data/movie_df_sequel_original.csv')

        for keyword_name in keywords_name:
            sync_to_movie_df(datas_extended, keyword_name, movie_df, wiki_id)
    else:
        randomly_sample_movie(start_date, end_date, 20000, "data/random_sample/random_sample_metadata_2010_2024.csv")


def sync_to_movie_df(datas_extended, keyword_name, movie_df, wiki_id):
    """
    Sync the data from the tmdb api to the wikipedia data, ensuring that the release year is the same and adding the
    missing box office revenue
    :param datas_extended: The extended data from the tmdb api containing the box office revenue
    :param keyword_name: the name of the keyword
    :param movie_df: the processed wikipedia data
    :param wiki_id: The database with the wikipedia id
    :return: None
    """
    data = wiki_id[keyword_name]
    movie_df_keyword = movie_df.join(data.set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_keyword = ensure_same_year(movie_df_keyword)
    movie_extended_df = datas_extended[keyword_name]
    movie_df_keyword = movie_df_keyword.apply(
        lambda x: fill_missing_value(x, movie_extended_df[movie_extended_df["id"] == x["id"]],
                                     "Movie box office revenue", "revenue"), axis=1)
    movie_df_keyword.to_csv(f'data/movie_df_{keyword_name}.csv')


def get_movies_from_tmdb(keywords, keywords_name, start_date, end_date):
    """
    Get the movies from the tmdb api
    :param keywords: The id of the keywords
    :param keywords_name: The string name of the keywords
    :param start_date: The start date of the movies format "YYYY-MM-DD"
    :param end_date: The end date of the movies format "YYYY-MM-DD"
    :return: The data from the tmdb api, the extended data from the tmdb api, and the metadata from the tmdb api in
    format given in the provided database
    """
    datas = {}
    datas_extended = {}
    meta_data_likes = {}
    years = f"{start_date[:4]}_{end_date[:4]}"

    for keyword, keyword_name in zip(keywords, keywords_name):
        keyword_name = keyword_name.replace(" ", "_")
        file_path = f"data/{keyword_name}"
        mkdir_no_exist(file_path)
        data = get_data(keyword_name, start_date, end_date, keyword, f"{file_path}/{keyword_name}_{years}.csv")
        data_extended = get_movie_data_extended(data, f"{file_path}/{keyword_name}_{years}_extended.csv")
        metadata = get_movie_metadatalike_db(data_extended, f"{file_path}/{keyword_name}_{years}_metadata.csv")

        datas[keyword_name] = data
        datas_extended[keyword_name] = data_extended
        meta_data_likes[keyword_name] = metadata

    return datas, datas_extended, meta_data_likes




