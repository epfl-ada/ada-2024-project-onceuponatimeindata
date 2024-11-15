import os

import pandas as pd
from nbconvert.filters import get_metadata
from sympy.physics.units import years
from tqdm import tqdm

from models.box_office_revenue import get_box_office_absolute, get_box_office_ratio, get_average_box_office_revenue, \
    compare_first_sequel
from models.collection_analysis import *

from models.collection_analysis import get_time_between_sequels
from models.movie_counter import get_movie_counter_figure, get_ratio_movie_figure
from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db, \
    randomly_sample_movie

from more_itertools import sliced
from src.data.TMDB_Movies import get_wikipedia_id_from_title
from src.models.movie_data_cleaner import display_data_cleaning_graph

if __name__ == "__main__":
    from src.models.movies_frame import MovieFrames

    movie_df = pd.read_csv('data/MovieSummaries/movie.metadata.tsv', sep='\t', header=None)
    new_movie_df = pd.read_csv('data/random_sample/random_sample_metadata_2010_2024.csv')



    keywords = ["sequels", "book", "comics", "remake"]
    path_old = []
    path_new = []

    for keyword in keywords:
        path_old.append(f"data/{keyword}/{keyword}_with_wiki_id_1880_2010.csv")
        path_new.append(f"data/{keyword}/{keyword}_metadata_2010_2024.csv")

    path_old.append("data/collections/sequels_and_original_with_wiki_id.csv")
    path_new.append("data/collections/sequels_and_original_metadata_2010_2024.csv")

    movie_frames_old = MovieFrames(movie_df, path_old, old=True)
    movie_frames_new = MovieFrames(new_movie_df, path_new)


    display_data_cleaning_graph(movie_frames_old)

    get_movie_counter_figure(movie_frames_new)

    get_ratio_movie_figure(movie_frames_old)

    get_box_office_absolute(movie_frames_old)

    get_box_office_ratio(movie_frames_old)

    get_average_box_office_revenue(movie_frames_old)

    compare_first_sequel(movie_frames_old)

    get_budget_vs_revenue(movie_frames_old)

    get_time_between_sequels(movie_frames_old)




