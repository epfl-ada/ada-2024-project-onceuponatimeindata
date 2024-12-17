import os

import pandas as pd
from nbconvert.filters import get_metadata
from tqdm import tqdm
import swifter


from data.TMDB_Movies import get_wikipedia_id_for_db, sample_all_movie
from data.dataset_enhancer import get_movies
from models.box_office_revenue import get_box_office_absolute, get_box_office_ratio, get_average_box_office_revenue, \
    compare_first_sequel
from models.collection_analysis import *

from models.collection_analysis import get_time_between_sequels
from models.genre_analysis import genre_type
from models.movie_counter import get_movie_counter_figure, get_ratio_movie_figure
from models.movies_frame import MovieFrames
from models.ratings_analysis import compare_first_sequel_ratings
from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db, \
    randomly_sample_movie

from more_itertools import sliced
from src.data.TMDB_Movies import get_wikipedia_id_from_title
from src.models.movie_data_cleaner import display_data_cleaning_graph

def p1():
    from src.models.movies_frame import MovieFrames

    movie_df = pd.read_csv('data/MovieSummaries_filtered/movie_df.csv')

    new_movie_df = pd.read_csv('data/all_sample/all_sample_2010_2024_metadata.csv')

    keywords = ["sequels", "book", "comics", "remake"]
    path_old = []
    path_new = []

    for keyword in keywords:
        path_old.append(f"data/{keyword}/{keyword}_1880_2010_with_wiki_id.csv")
        path_new.append(f"data/{keyword}/{keyword}_2010_2024_metadata.csv")

    path_old.append("data/collections/sequels_and_original_1880_2010_with_wiki_id.csv")
    path_new.append("data/collections/sequels_and_original_2010_2024_metadata.csv")

    movie_frames_old = MovieFrames(movie_df, path_old, 1880, 2010)
    movie_frames_new = MovieFrames(new_movie_df, path_new, 2010, 2024)

    extended_path = ["data/sequels/sequels_1880_2010_extended.csv", "data/sequels/sequels_2010_2024_extended.csv",
                        "data/collections/sequels_and_original_1880_2010_extended.csv", "data/collections/sequels_and_original_2010_2024_extended.csv",
                        "data/book/book_1880_2010_extended.csv", "data/book/book_2010_2024_extended.csv",
                        "data/comics/comics_1880_2010_extended.csv", "data/comics/comics_2010_2024_extended.csv",
                        "data/remake/remake_1880_2010_extended.csv", "data/remake/remake_2010_2024_extended.csv",
                        "data/all_sample/all_sample_2010_2024_extended.csv"]

    fig = display_data_cleaning_graph(movie_frames_old)
    movie_frames_new.drop_different_years()
    movie_frames_new.drop_impossible_years()
    movie_frames_concat = movie_frames_old.concat_movie_frame(movie_frames_new)
    fig = get_movie_counter_figure(movie_frames_concat)
    genre_type(movie_frames_concat, extended_path, debug=True)

def p2():
    keywords_name = ["sequels", "book", "comics", "remake"]
    datas = {}
    wiki_id = {}
    start_date = "1880-01-01"
    end_date = "2010-01-01"
    years = "1880_2010"

    for keyword_name in keywords_name:
        datas[keyword_name] = pd.read_csv(f'data/{keyword_name}/{keyword_name}_{start_date[:4]}_{end_date[:4]}.csv')
    for data, keyword_name in zip(datas.values(), datas.keys()):
        file_name = f"{keyword_name}_{years}_with_wiki_id_updated.csv"
        wiki_id[keyword_name] = get_wikipedia_id_for_db(data, f"data/{keyword_name}/{file_name}")

    get_wikipedia_id_for_db(pd.read_csv('data/collections/sequels_and_original_1880_2010.csv'), f"data/collections/sequels_and_original_{years}_with_wiki_id.csv")


if __name__ == "__main__":
    p1()