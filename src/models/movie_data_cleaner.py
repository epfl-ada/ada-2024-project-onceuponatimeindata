import numpy as np
from docutils.nodes import legend
from docutils.parsers.rst.directives.tables import align
from matplotlib.pyplot import yscale
from plotly import graph_objects as go
from matplotlib.colors import to_rgb
from sphinx.util.console import coloron

from utils.evaluation_utils import rgb_string_to_array, array_to_rgb_string


# function to create the graph

def create_graph(TMDB_sizes, Wikipedia_sizes, movie_errors_sizes, get_color):
    """
    Create a graph with the sizes of the dataframes
    :param TMDB_sizes: dataframes sizes before cleaning
    :param Wikipedia_sizes: dataframes sizes after cleaning
    :param movie_errors_sizes: dataframes sizes after dropping the movies with different years
    :param get_color: function to get the color
    :return: figure with the graph
    """
    width = 0.3
    ind = np.arange(5)

    fig = go.Figure()
    colors1 = [get_color("Sequels and Original"), get_color("Sequels"), get_color("Book Adaptation"), get_color("Comics Adaptation"), get_color("Remake")]
    colors2 = [array_to_rgb_string(rgb_string_to_array(color) *9/10) for color in colors1]
    colors3 = [array_to_rgb_string(rgb_string_to_array(color) *8/10) for color in colors1]

    fig.add_trace(go.Bar(
        x=ind,
        y=TMDB_sizes,
        width=width,
        name='TMDB',
        marker_color=colors1,
    ))

    fig.add_trace(go.Bar(
        x=ind + width,
        y=Wikipedia_sizes,
        width=width,
        name='Wikipedia',
        marker_color=colors2,
    ))

    fig.add_trace(go.Bar(
        x=ind + 2 * width,
        y=movie_errors_sizes,
        width=width,
        name='After filtering',
        marker_color=colors3,
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
        height=500,
        showlegend=False,
    )

    return fig


def create_movie_lost_graph(movie_lost_list, get_color):
    """
    Create a graph with the movies that were lost during the data cleaning
    :param movie_lost_list: dictionnary with the movies that were lost
    """
    # graph per year
    fig = go.Figure()
    for name, movie_df in movie_lost_list.items():
        movie_df["Movie year"] = movie_df["release_date"].apply(lambda x: float(str(x)[:4]))
        movie_df = movie_df[movie_df["Movie year"] < 2010]
        movie_df_count_year = movie_df.groupby("Movie year").count()
        fig.add_trace(go.Scatter(
            x=movie_df_count_year.index,
            y=movie_df_count_year["title"],
            mode='lines',
            name=f"Number of {name} lost",
            line=dict(color=get_color(name)),
            stackgroup='one',
        ))
    fig.update_layout(
        title='Number of movies lost during data cleaning',
        xaxis_title='Year',
        yaxis_title='Number of movies',
        width=800,
        height=500,
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

    movie_lost_list = movieFrames.match_movie_df()

    # Get the sizes of the dataframes after matching

    wikipedia_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                          len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                          len(movieFrames.movie_df_remakes)]

    # Drop the movies that have different years in TMDB and Wikipedia

    movieFrames.drop_different_years()
    movieFrames.drop_impossible_years()
    movieFrames.drop_too_different_titles()

    # Get the sizes of the dataframes after dropping the movies with different years

    movie_errors_sizes = [len(movieFrames.movie_df_sequel_original), len(movieFrames.movie_df_sequel_only),
                            len(movieFrames.movie_df_books), len(movieFrames.movie_df_comics),
                            len(movieFrames.movie_df_remakes)]

    # Create the graph

    fig = create_graph(TMDB_sizes, wikipedia_sizes, movie_errors_sizes, movieFrames.get_color_discrete)
    fig_lost = create_movie_lost_graph(movie_lost_list, movieFrames.get_color_discrete)
    return fig, fig_lost