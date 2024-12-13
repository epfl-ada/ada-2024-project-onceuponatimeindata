import os

import pandas as pd
from nbconvert.filters import get_metadata
from sympy.physics.units import years
from tqdm import tqdm

from data.dataset_enhancer import get_movies
from models.box_office_revenue import get_box_office_absolute, get_box_office_ratio, get_average_box_office_revenue, \
    compare_first_sequel
from models.collection_analysis import *

from models.collection_analysis import get_time_between_sequels
from models.movie_counter import get_movie_counter_figure, get_ratio_movie_figure, get_merge_movie_counter_figure
from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db, \
    randomly_sample_movie

from more_itertools import sliced
from src.data.TMDB_Movies import get_wikipedia_id_from_title
from src.models.movie_data_cleaner import display_data_cleaning_graph

if __name__ == "__main__":
    from src.models.movies_frame import MovieFrames

    movie_df = pd.read_csv('data/MovieSummaries_filtered/movie_df.csv')

    new_movie_df = pd.read_csv('data/random_sample/random_sample_2010_2024_metadata.csv')

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

    display_data_cleaning_graph(movie_frames_old)
    get_movie_counter_figure(movie_frames_old)
    get_movie_counter_figure(movie_frames_new, split=5)
    fig = get_merge_movie_counter_figure(movie_frames_old, movie_frames_new, split=5)