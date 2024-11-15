from src.scripts.script_to_get_data import *

process_movie_data_from_TMDB()

# Function that adds Wikipedia ID for each movie, books, comics, remakes

process_movie_data(
        movie_metadata_path='data/MovieSummaries/movie.metadata.tsv',
        sequel_collection_path='data/collections/sequels_and_original_with_wiki_id.csv',
        sequel_with_wiki_id_path='data/movie_with_keyword_sequel_with_wiki_id.csv',
        book_with_wiki_id_path='data/book/book_with_wiki_id_1880_2010.csv',
        comics_with_wiki_id_path='data/comics/comics_with_wiki_id_1880_2010.csv',
        remake_with_wiki_id_path='data/remake/remake_with_wiki_id.csv',
        output_folder='data/processed_movies'
    )

remove_movies_same_year_btw_wiki_tmdb()

fill_missing_value_in_dataframe()   

