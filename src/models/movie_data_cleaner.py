import numpy as np
from matplotlib import pyplot as plt

# function to create the graph

def create_graph(TMDB_sizes, Wikipedia_sizes, movie_errors_sizes):
    """
    Create a graph with the sizes of the dataframes
    :param TMDB_sizes: dataframes sizes before cleaning
    :param Wikipedia_sizes: dataframes sizes after cleaning
    :param movie_errors_sizes: dataframes sizes after dropping the movies with different years
    :return: figure with the graph
    """
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
    """
    Display the graph with the sizes of the dataframes
    :param movieFrames: the MovieFrames class with the dataframes
    :return: the figure with the graph
    """

    # Get the sizes of the dataframes

    TMDB_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                  len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                  len(movieFrames.movie_df_remakes)]

    # Match the dataframes

    movieFrames.match_movie_df()

    # Get the sizes of the dataframes after matching

    wikipedia_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                          len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                          len(movieFrames.movie_df_remakes)]

    # Drop the movies that have different years in TMDB and Wikipedia

    movieFrames.drop_different_years()

    # Get the sizes of the dataframes after dropping the movies with different years

    movie_errors_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                            len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                            len(movieFrames.movie_df_remakes)]

    # Create the graph

    fig = create_graph(TMDB_sizes, wikipedia_sizes, movie_errors_sizes)
    return fig