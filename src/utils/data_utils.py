import fuzzywuzzy.fuzz
from rapidfuzz import fuzz
import swifter
import pandas as pd
from tqdm import tqdm


def find_similar_movies(df, movie_df):
    """
    Find the movies with similar titles and the same release year
    :param df: the dataframe with the movies
    :param movie_df: the movie dataframe
    """
    df_out = None

    def process_movie(movie):
        title = movie["title"]
        year = str(movie["release_date"])[:4]

        same_year = movie_df[movie_df["Movie release date"].str.contains(year).fillna(False)]
        similar_movies = same_year[same_year["Movie name"].apply(lambda x: fuzz.ratio(title, x)) > 90]

        if len(similar_movies) == 1:
            line = similar_movies.iloc[0].to_frame().transpose()
            for column in movie.index:
                if column == "Wikipedia movie ID":
                    continue
                line[column] = movie[column]
            return line
        return None

    df_out = pd.concat(df.swifter.apply(lambda movie: process_movie(movie), axis=1).dropna().tolist(),
                       ignore_index=True)
    return df_out