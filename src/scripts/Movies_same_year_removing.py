from src.data.Removed_movies_same_year import *

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

