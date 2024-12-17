import pandas as pd
from plotly import graph_objects as go

from models.box_office_revenue import get_compare_first_sequel_graph_plotly

def get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, get_colors):
    """
    plot the box office revenue of the first movie and the sequel movie
    :param first_vs_rest: the dataframe with the box office revenue
    :param average_rating: the average rating of a movie
    :param get_colors: function to get the color
    :return: the figure with the plot
    """
    fig_avg = go.Figure()
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest_avg"]

    text_first = first_vs_rest.index + "<br>First movie box average rating: " + y1.astype(str)
    text_sequel = first_vs_rest.index + "<br>Average sequel movie rating average: " + y2.astype(str)

    fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie rating",
                                 text=text_first, marker_color=get_colors("Movie"), hoverinfo="text"))
    fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie rating",
                                 text=text_sequel, marker_color=get_colors("Sequels"), hoverinfo="text"))

    for i in range(len(x)):
        if y1[i] > y2[i]:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="lightcoral", width=1))
        else:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="palegreen", width=1))

    fig_avg.add_hline(y=average_rating, line_dash="dot", line_color="peru",
                      name="Average rating of a movie", annotation_text="Average rating of a movie",)

    fig_avg.add_hline(y=y2.mean(), line_dash="dot", line_color="blue",
                        name="Average rating of a sequel movie", annotation_text="Average rating of a sequel movie",)

    fig_avg.add_hline(y=y1.mean(), line_dash="dot", line_color="red",
                        name="Average rating of a first movie", annotation_text="Average rating of a first movie",)

    fig_avg.update_layout(
        title="First movie vs Average sequel movie box office revenue",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        width=1000,
        height=600,
        legend=dict(
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        )
    )
    return fig_avg


def compare_first_sequel_ratings(movie_frame, ratings_path_list):
    """
    compare the box office revenue of the first movie and the sequel movie
    :param movie_frame: the database with the movies
    :param ratings_path_list: list of files with additional ratings information
    :return: the figure with the plot
    """

    for ratings_path in ratings_path_list:
        ratings = pd.read_csv(ratings_path)
        movie_frame.movie_df_sequel_original = pd.merge(movie_frame.movie_df_sequel_original, ratings[["id", "vote_average"]],
                                                        on="id", how="inner") if "vote_average" not in movie_frame.movie_df_sequel_original.columns \
                                                        else movie_frame.movie_df_sequel_original


    # calculate the box office revenue for the first movie of each collection
    box_office_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        "vote_average"]

    # calculate the remaining box office revenue for each collection # inflation adj

    box_office_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["vote_average"].agg(
        'sum') - box_office_first_movie

    # calculate the remaining box office revenue for each collection (excluding the first movie)

    box_office_remainder_avg = box_office_remainder / (
                movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

    first_vs_rest = pd.DataFrame()
    first_vs_rest["first"] = box_office_first_movie
    first_vs_rest["rest"] = box_office_remainder
    first_vs_rest["rest_avg"] = box_office_remainder_avg
    first_vs_rest = first_vs_rest.dropna()
    first_vs_rest = first_vs_rest[first_vs_rest["first"] > 0]  # remove collections with no ratings
    first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0]
    first_vs_rest = first_vs_rest[first_vs_rest["rest_avg"] > 0]
    first_vs_rest = first_vs_rest.sort_values("first",
                                              ascending=True)  # sort in ascending order for the first movie (lowest to the highest)
    first_vs_rest['index'] = range(0, len(first_vs_rest))

    average_rating = movie_frame.movie_df_sequel_original["vote_average"].mean()

    fig_avg = get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, movie_frame.get_color_discrete)
    return fig_avg