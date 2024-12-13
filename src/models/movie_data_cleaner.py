import numpy as np
from docutils.parsers.rst.directives.tables import align
from plotly import graph_objects as go

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
    ind = np.arange(5)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=ind,
        y=TMDB_sizes,
        width=width,
        name='TMDB'
    ))

    fig.add_trace(go.Bar(
        x=ind + width,
        y=Wikipedia_sizes,
        width=width,
        name='Wikipedia'
    ))

    fig.add_trace(go.Bar(
        x=ind + 2 * width,
        y=movie_errors_sizes,
        width=width,
        name='After filtering'
    ))

    fig.add_annotation(
        text = f"The TMDB dataset has <br>{TMDB_sizes[2]} movies based on books or novels",
        x = 2,
        y = TMDB_sizes[2],
        showarrow = True,
        arrowhead = 1
    )
    fig.add_annotation(
        text = f"after cleaning, <br>{movie_errors_sizes[2]} movies are found <br> in the database",
        x = 2 + 2 * width,
        y = movie_errors_sizes[2],
        showarrow = True,
        arrowhead = 1,
        ax = 40,  # Adjust this value to change the angle
        ay = -40  # Adjust this value to change the angle
    )


    fig.update_layout(
        title='Size differences during data prepossessing',
        xaxis=dict(
            tickvals=ind + width,
            ticktext=["Sequel\ncollections", "Sequels", "Books", "Comics", "Remakes"]
        ),
        xaxis_title='Dataset',
        yaxis_title='Number of movies',
        barmode='group',
        width=800,
        height=500
    )

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