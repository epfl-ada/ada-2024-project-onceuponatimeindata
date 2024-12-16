import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from numpy.core.defchararray import title
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from src.models.movies_frame import MovieFrames


def movies_per_year(df : pd.DataFrame,  start_year : int, end_year : int, interval : int = 5) -> tuple:
    """
    Group movies by release year and count the number of movies per year
    :param df:  dataframe with the movies
    :param start_year: start year
    :param end_year: end year
    :param interval: number of years per group
    :return: 
    """

    movies_per_years_df = df.groupby(pd.cut(df["release year"], np.arange(start_year, end_year+interval, interval))).count()
    years = movies_per_years_df.index.astype(str)
    years = [x[1:][:-1] for x in years]
    return movies_per_years_df, years

def figure_movie_year(df, movie_type, years, fig, split = 5):
    """
    Plot the number of movies per year
    :param df: dataframe with the movies
    :param movie_type: Type of movie
    :param years: release years
    :param fig: figure to plot
    :param split: The number of years per group
    :return: the axis with the plot
    """
    colors = px.colors.cyclical.Twilight
    marker_colors = {
        "movies": colors[6],
        "sequels": colors[1],
        "books": colors[2],
        "comics": colors[3],
        "remakes": colors[4],
        "all non-original movies": colors[5],
    }

    fig.add_trace(go.Bar(
        x=years,
        y=df["Movie name"],
        name=f"Number of {movie_type} per {split} years",
        visible="legendonly",
        marker_color=marker_colors[movie_type]
    ))

    return fig

def get_movie_counter_data(movie_frames : MovieFrames, split = 5):
    movie_df = movie_frames.movie_df

    movie_df_sequel_only = movie_frames.movie_df_sequel_only
    movie_df_books = movie_frames.movie_df_books
    movie_df_comics = movie_frames.movie_df_comics
    movie_df_remakes = movie_frames.movie_df_remakes

    # add release year to the dataframes
    movie_frames.add_release_year()

    # grouping and count movies by release year 1890-2010
    movies_per_years, movies_years = movies_per_year(movie_df, movie_frames.start_year, movie_frames.end_year,
                                                     interval=split)
    sequel_per_year, sequel_years = movies_per_year(movie_df_sequel_only, movie_frames.start_year,
                                                    movie_frames.end_year, interval=split)
    book_per_year, book_years = movies_per_year(movie_df_books, movie_frames.start_year, movie_frames.end_year,
                                                interval=split)
    comics_per_year, comics_years = movies_per_year(movie_df_comics, movie_frames.start_year, movie_frames.end_year,
                                                    interval=split)
    remakes_per_year, remakes_years = movies_per_year(movie_df_remakes, movie_frames.start_year, movie_frames.end_year,
                                                      interval=split)

    return movies_per_years, movies_years, sequel_per_year, sequel_years, book_per_year, book_years, comics_per_year, comics_years, remakes_per_year, remakes_years

def get_button(x, y, max_movies, max_variants, max_combined):
    button = list([
        dict(type="buttons",
             direction="left",
             buttons=[dict(label="Movies",
                           method="update",
                           args=[{"visible": [True, False, False, False, False, False]},
                                 {"yaxis": dict(range=[0, max_movies], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}]),
                      dict(label="Sequels",
                           method="update",
                           args=[{"visible": [False, True, False, False, False, False]},
                                 {"yaxis": dict(range=[0, max_variants], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}]),
                      dict(label="Books",
                           method="update",
                           args=[{"visible": [False, False, True, False, False, False]},
                                 {"yaxis": dict(range=[0, max_variants], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}]),
                      dict(label="Comics",
                           method="update",
                           args=[{"visible": [False, False, False, True, False, False]},
                                 {"yaxis": dict(range=[0, max_variants], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}]),
                      dict(label="Remakes",
                           method="update",
                           args=[{"visible": [False, False, False, False, True, False]},
                                 {"yaxis": dict(range=[0, max_variants], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}]),
                      dict(label="All non-original movies",
                           method="update",
                           args=[{"visible": [False, False, False, False, False, True]},
                                 {"yaxis": dict(range=[0, max_combined], title="Number of movies")},
                                 {"xaxis" : dict(title="Year", tickangle=45)}],
                           ),
                      ],

             pad={"r": 10, "t": 10},
             showactive=True,
             x=x,
             xanchor="left",
             y=y,
             yanchor="top"
             ),
    ])
    return button


def figure_tendency(movies_per_years, name, movies_years, fig, split):
    """
    Plot the tendency of the number of movies per year
    :param movies_per_years: dataframe with the number of movies per year
    :param name: name of function to plot
    :param movies_years: release years
    :param fig: figure to plot
    :param split: number of years per group
    :return: the axis with the plot
    """
    colors = px.colors.cyclical.Twilight
    marker_colors = {
        "movies": colors[7],
        "sequels": colors[2],
        "books": colors[3],
        "comics": colors[4],
        "remakes": colors[5],
        "all non-original movies": colors[6],
    }

    poly = PolynomialFeatures(degree=2)
    x = np.arange(int(movies_years[0][:4]), int(movies_years[-1][:4]), 5)
    x_pred = np.arange(int(movies_years[0][:4]), int(movies_years[-1][-4:]), 5)
    y = np.array(movies_per_years["Movie name"])[:-1]
    poly_features = poly.fit_transform(x.reshape(-1, 1))
    x_pred_poly = poly.transform(x_pred.reshape(-1, 1))

    model = LinearRegression()
    model.fit(poly_features, y)
    y_out = model.predict(x_pred_poly)

    fig.add_trace(go.Scatter(x=movies_years, y=y_out,
                                mode='lines', name=f"{name} tendency",
                                line=dict(color=marker_colors[name], width=2),
                                visible="legendonly",
                                marker_color=marker_colors[name],
                                text=f"R2 score: {model.score(poly_features, y)}",
                                hoverinfo='text'))

    return fig


def get_movie_counter_figure(movie_frames : MovieFrames, split = 5):
    """
    plot the number of movies per year
    :param movie_frames: MovieFrames class with the movies
    :param split: 
    :return:
    """

    (movies_per_years, movies_years,
        sequel_per_year, sequel_years,
        book_per_year, book_years,
        comics_per_year, comics_years,
        remakes_per_year, remakes_years) = get_movie_counter_data(movie_frames, split)

    fig = go.Figure()

    figure_movie_year(movies_per_years, "movies", movies_years, fig, split)
    figure_movie_year(sequel_per_year, "sequels", sequel_years, fig, split)
    figure_movie_year(book_per_year, "books", book_years, fig, split)
    figure_movie_year(comics_per_year, "comics", comics_years, fig, split)
    figure_movie_year(remakes_per_year, "remakes", remakes_years, fig, split)
    figure_movie_year(sequel_per_year + book_per_year + comics_per_year + remakes_per_year,
                      "all non-original movies", sequel_years, fig, split)


    figure_tendency(movies_per_years, "movies", movies_years, fig, split)
    figure_tendency(sequel_per_year, "sequels", sequel_years, fig, split)
    figure_tendency(book_per_year, "books", book_years, fig, split)
    figure_tendency(comics_per_year, "comics", comics_years, fig, split)
    figure_tendency(remakes_per_year, "remakes", remakes_years, fig, split)
    figure_tendency(sequel_per_year + book_per_year + comics_per_year + remakes_per_year,
                    "all non-original movies", sequel_years, fig, split)


    #choose between figures
    data = [trace for trace in fig.data]

    update_menu = get_button(0, 1.2, movies_per_years["Movie name"].max() + 100,
                             max(sequel_per_year["Movie name"].max(), book_per_year["Movie name"].max(),
                                 comics_per_year["Movie name"].max(), remakes_per_year["Movie name"].max()),
                                (sequel_per_year + book_per_year + comics_per_year + remakes_per_year)["Movie name"].max() + 10)

    layout = dict(updatemenus=update_menu,
                  xaxis=dict(
                        tickvals=movies_years,
                        tickangle=45
                  ),
                    title=f"Number of movies per {split} years splits",
                    xaxis_title="Year",
                    )

    fig = go.Figure(data=data, layout=layout)

    return fig

    

def plot_ratio(movie_frame, split=5):
    """
    Plot of the ratio of movies with sequels per 5 year
    :param movie_frame: dataframe with the movies
    :param split: number of years per group
    :return: figure with the plot
    """
    movie_df = movie_frame.movie_df
    movie_df = movie_df.dropna(subset=["release year"])
    movies_per_years = movie_df.groupby(pd.cut(movie_df["release year"], np.arange(movie_frame.start_year, movie_frame.end_year + split, split))).count()

    ratios = []
    for df in movie_frame.get_all_alternate_df():
        movies_alternate_per_year = df.groupby(pd.cut(df["release year"], np.arange(movie_frame.start_year,
                                                                                   movie_frame.end_year + split, split))).count()

        years = movies_per_years.index.astype(str)
        years = [x[1:][:-1] for x in years]

        movie_df_ratio = movies_alternate_per_year / movies_per_years * 100
        movie_df_ratio = movie_df_ratio.fillna(0)
        ratios.append(movie_df_ratio)

    fig = go.Figure()

    i = 0
    for movie_df_ratio, name in zip(ratios, movie_frame.get_all_alternate_df_names()):
        fig.add_trace(go.Scatter(x=years, y=movie_df_ratio["Movie name"],
                                 mode='lines+markers', name=f"ratio of {str.lower(name)} per movies",
                                 line=dict(color=px.colors.qualitative.Set2[i], width=2)))
        i += 1
    fig.update_layout(title=f"Ratio of movies per {split} years",
                      xaxis_title="Year",
                      yaxis_title="Ratio (%)",
                      xaxis=dict(
                          tickvals=years,
                          tickangle=45
                      ))

    return fig

def get_ratio_movie_figure(movie_frames : MovieFrames):
    movie_frames.add_release_year()
    return plot_ratio(movie_frames)
