import numpy as np
from matplotlib import pyplot as plt


def create_graph(TMDB_sizes, Wikipedia_sizes, movie_errors_sizes):
    width = 0.3

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(221)

    ind = np.arange(5)

    ax.bar(ind, TMDB_sizes, width=width, label="TMDB")
    ax.bar(ind + width, Wikipedia_sizes, width=width, label="Wikipedia")
    ax.bar(ind + 2 * width, movie_errors_sizes, width=width, label="After filtering")

    plt.xticks(ind + width, ["Sequel\ncollections", "Sequels", "Books", "Comics", "Remakes"])

    ax.legend()
    ax.title.set_text("Size differences during data prepossessing")
    ax.set_xlabel("Dataset")
    ax.set_ylabel("Number of movies")

    return fig

def display_data_cleaning_graph(movieFrames):

    TMDB_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                  len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                  len(movieFrames.movie_df_remakes)]

    movieFrames.match_movie_df()

    wikipedia_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                          len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                          len(movieFrames.movie_df_remakes)]

    movieFrames.drop_different_years()

    movie_errors_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                            len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                            len(movieFrames.movie_df_remakes)]

    fig = create_graph(TMDB_sizes, wikipedia_sizes, movie_errors_sizes)
    return fig