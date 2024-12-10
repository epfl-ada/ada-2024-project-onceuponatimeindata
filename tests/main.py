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
from models.movie_counter import get_movie_counter_figure, get_ratio_movie_figure
from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db, \
    randomly_sample_movie

from more_itertools import sliced
from src.data.TMDB_Movies import get_wikipedia_id_from_title
from src.models.movie_data_cleaner import display_data_cleaning_graph

if __name__ == "__main__":
    from src.models.movies_frame import MovieFrames

    keywords_name = ["sequels", "book", "comics", "remake"]
    keywords = [9663, 818, 9717,
                9714]  # keywords for the movies corresponding to the sequels, book or novel adaptations, and based on comics, and remakes

    start_date = "1880-01-01"
    end_date = "2010-01-01"

    get_movies(keywords_name, keywords, start_date, end_date)

    start_date = "2010-01-01"
    end_date = "2024-01-01"
    get_movies(keywords_name, keywords, start_date, end_date)



