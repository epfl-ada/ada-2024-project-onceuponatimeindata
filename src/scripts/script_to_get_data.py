from src.data.Data_collecting_from_TMDB import *
from src.data.Movies_wikipedia_ID_adding import *
from src.data.TMDB_Movies import *
from src.data.Removed_movies_same_year import *


# Function that processes movie data for specified keywords

def process_movie_data_from_TMDB():

    keywords_name = ["sequels", "book", "comics", "remake"]
    keywords = [9663, 818, 9717, 9714]  # IDs for the respective categories
    process_movie_data(keywords_name, keywords)

    # Function that processes sequel movies by reading CSV files and generating collections

    file_paths = [
            "data/sequels/movie_with_sequels_1880_2010.csv",
            "data/sequels/movie_with_sequels_2010_2024.csv"
        ]
    years = ["1880_2010", "2010_2024"]
    process_sequels_movies(file_paths, years)

    # Process the sequel collections
    sequel_collections = pd.read_csv('data/collections/sequels.csv')
    sequel_collections_with_wiki_id = get_wikipedia_id_for_db(sequel_collections, "data/collections/sequels_and_original_with_wiki_id.csv")
    sequel_collections_with_wiki_id.to_csv('data/collections/sequels_and_original_with_wiki_id.csv')
    print("Sequel collections processed.")

    # Process the sequels
    sequels = pd.read_csv('data/movie_with_keyword_sequel.csv')
    sequels_with_wiki_id = get_wikipedia_id_for_db(sequels, 'data/movie_with_keyword_sequel_with_wiki_id.csv')
    sequels_with_wiki_id.to_csv('data/movie_with_keyword_sequel_with_wiki_id.csv')
    print("Sequels processed.")

    # Process the books
    book = pd.read_csv("data/book/movie_with_book_1880_2010.csv")
    book_with_wiki_id = get_wikipedia_id_for_db(book, 'data/book/book_with_wiki_id_1880_2010.csv')
    book_with_wiki_id.to_csv('data/book/book_with_wiki_id_1880_2010.csv')
    print("Books processed.")

    # Process the comics
    comics = pd.read_csv("data/comics/movie_with_comics_1880_2010.csv")
    comics_with_wiki_id = get_wikipedia_id_for_db(comics, 'data/comics/comics_with_wiki_id_1880_2010.csv')
    comics_with_wiki_id.to_csv('data/comics/comics_with_wiki_id_1880_2010.csv')
    print("Comics processed.")

    # Process the remakes
    remake = pd.read_csv("data/remake/movie_with_remake_1880_2010.csv")
    remake_with_wiki_id = get_wikipedia_id_for_db(remake, 'data/remake/remake_with_wiki_id.csv')
    remake_with_wiki_id.to_csv('data/remake/remake_with_wiki_id.csv')
    print("Remakes processed.")
   

# Function that processes sequel movies by reading CSV files and generating collections

def remove_movies_same_year_btw_wiki_tmdb():
    movie_df_sequel_only = ensure_same_year(movie_df_sequel_only)
    movie_df_sequel_only.to_csv('data/movie_df_sequel_only.csv')
    print("Sequel only movies processed.")

    movie_df_sequel_original = ensure_same_year(movie_df_sequel_original)
    movie_df_sequel_original.to_csv('data/movie_df_sequel_original.csv')
    print("Sequel original movies processed.")

    movie_df_book = ensure_same_year(movie_df_book)
    movie_df_book.to_csv('data/movie_df_book.csv')
    print("Book movies processed.")

    movie_df_comics = ensure_same_year(movie_df_comics)
    movie_df_comics.to_csv('data/movie_df_comics.csv')
    print("Comics movies processed.")

    movie_df_remake = ensure_same_year(movie_df_remake)
    movie_df_remake.to_csv('data/movie_df_remake.csv')
    print("Remake movies processed.")

# function to fill missing values in the dataset

def fill_missing_value_in_dataframe():
    movie_extended_df = pd.read_csv("data/collections/sequels_extended_1880_2010.csv")
    movie_df_sequel_original.apply(lambda x : fill_missing_value(x, movie_extended_df[movie_extended_df["id"] == x["id"]], "Movie box office revenue","revenue"), axis=1)
    print("Missing values filled for movie_df_sequel_original")

    sequels_only_extended_df = pd.read_csv("data/sequels/sequels_extended.csv")
    movie_df_sequel_only.apply(lambda x : fill_missing_value(x, sequels_only_extended_df[sequels_only_extended_df["id"] == x["id"]], "Movie box office revenue","revenue"), axis=1)
    print("Missing values filled for movie_df_sequel_only")