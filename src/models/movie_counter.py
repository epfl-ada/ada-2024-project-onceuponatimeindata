import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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

    movies_per_years_df = df.groupby(pd.cut(df["release year"], np.arange(start_year, end_year, interval))).count()
    years = movies_per_years_df.index.astype(str)
    years = [x[1:][:-1] for x in years]
    return movies_per_years_df, years

def figure_movie_year(df, movie_type, years, ax_f, split = 5):
    """
    Plot the number of movies per year
    :param df: dataframe with the movies
    :param movie_type: Type of movie
    :param years: release years
    :param ax_f: the axis to plot the figure
    :param split: The number of years per group
    :return: the axis with the plot
    """
    ax_f.bar(years, df["Movie name"], label=f"Number of {movie_type}")
    ax_f.legend()
    ax_f.title.set_text(f"Number of {movie_type} per {split} years splits")
    ax_f.set_xlabel("Year")
    ax_f.set_ylabel("Number of movies")
    start_year = [int(x[:4]) for x in years]
    ax_f.set_xticks(years, labels=start_year, rotation = 90)
    return ax_f

def get_movie_counter_figure(movie_frames : MovieFrames, split = 5):
    """
    plot the number of movies per year
    :param movie_frames: MovieFrames class with the movies
    :param split: 
    :return: 
    """

    movie_df = movie_frames.movie_df

    movie_df_sequel_only = movie_frames.movie_df_sequel_only
    movie_df_books = movie_frames.movie_df_books
    movie_df_comics = movie_frames.movie_df_comics
    movie_df_remakes = movie_frames.movie_df_remakes

    # add release year to the dataframes
    movie_frames.add_release_year()

    # grouping and count movies by release year 1890-2010
    movies_per_years, movies_years = movies_per_year(movie_df, movie_frames.start_year, movie_frames.end_year, interval=split)
    sequel_per_year, sequel_years = movies_per_year(movie_df_sequel_only, movie_frames.start_year, movie_frames.end_year, interval=split)
    book_per_year, book_years = movies_per_year(movie_df_books, movie_frames.start_year, movie_frames.end_year, interval=split)
    comics_per_year, comics_years = movies_per_year(movie_df_comics, movie_frames.start_year, movie_frames.end_year, interval=split)
    remakes_per_year, remakes_years = movies_per_year(movie_df_remakes, movie_frames.start_year, movie_frames.end_year, interval=split)


    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(8, 14))
    ax1 = figure_movie_year(movies_per_years, "movies", movies_years, ax1)
    ax2 = figure_movie_year(sequel_per_year, "sequels", sequel_years, ax2)
    ax3 = figure_movie_year(book_per_year, "books", book_years, ax3)
    ax4 = figure_movie_year(comics_per_year, "comics", comics_years, ax4)
    ax5 = figure_movie_year(remakes_per_year, "remakes", remakes_years, ax5)
    ax6 = figure_movie_year(sequel_per_year + book_per_year + comics_per_year + remakes_per_year,
                            "all non-original movies", sequel_years, ax6)

    return fig



def plot_ratio(movie_df, df, split=5):
    """
    Plot of the ratio of movies with sequels per 5 year
    """
    movies_per_years = movie_df.groupby(pd.cut(movie_df["release year"], np.arange(1885, 2011, split))).count()
    movies_sequel_per_year = df.groupby(pd.cut(df["release year"], np.arange(1885, 2011, split))).count()

    years = movies_per_years.index.astype(str)
    years = [x[1:][:-1] for x in years]

    movie_df_ratio = movies_sequel_per_year / movies_per_years * 100
    movie_df_ratio = movie_df_ratio.fillna(0)

    fig = plt.figure(figsize=(8, 6))

    ax = fig.add_subplot(111)
    ax.plot(years, movie_df_ratio["Wikipedia movie ID"])
    ax.title.set_text(f"Ratio of movies with sequels per {split} years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Ratio")
    start_year = [int(x[:4]) for x in years]
    ax.set_xticks(years, labels=start_year, rotation = 90)
    return fig

def get_ratio_movie_figure(movie_frames : MovieFrames):
    movie_frames.add_release_year()
    return plot_ratio(movie_frames.movie_df, movie_frames.movie_df_sequel_only)
