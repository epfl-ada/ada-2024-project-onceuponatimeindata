import numpy as np
import pandas as pd
from rich.jupyter import display


class MovieFrames:
    movie_df : pd.DataFrame
    movie_df_sequel_only : pd.DataFrame
    movie_df_books : pd.DataFrame
    movie_df_comics : pd.DataFrame
    movie_df_remakes : pd.DataFrame
    movie_df_sequel_original : pd.DataFrame

    def __init__(self, movie_df, alternate_df : list, old = False):

        self.movie_df = movie_df
        if(old):
            self.movie_df = self.rename_columns(self.movie_df)

        for df in alternate_df:
            if "book" in df:
                self.movie_df_books = pd.read_csv(df)
            elif "comics" in df:
                self.movie_df_comics = pd.read_csv(df)
            elif "remake" in df:
                self.movie_df_remakes = pd.read_csv(df)
            elif "sequel" in df and "original" in df:
                self.movie_df_sequel_original = pd.read_csv(df)
            elif "sequel" in df:
                self.movie_df_sequel_only = pd.read_csv(df)


    def add_release_year(self):
        """
        Add a column with the release year to the dataframes
        """

        self.movie_df = self.add_release_year_df(self.movie_df, "Movie release date")
        self.movie_df_sequel_only = self.add_release_year_df(self.movie_df_sequel_only, "Movie release date")
        self.movie_df_books = self.add_release_year_df(self.movie_df_books, "Movie release date")
        self.movie_df_comics = self.add_release_year_df(self.movie_df_comics, "Movie release date")
        self.movie_df_remakes = self.add_release_year_df(self.movie_df_remakes, "Movie release date")
        self.movie_df_sequel_original = self.add_release_year_df(self.movie_df_sequel_original, "Movie release date")

    def add_release_year_df(self, df : pd.DataFrame, column_name : str) -> pd.DataFrame:
        """
        Add a column with the release year to the dataframe
        """
        if "release year" in df.columns:
            return df
        if column_name not in df.columns:
            print(f"Column {column_name} not found in the dataframe with columns {df.columns}")
            return df
        df["release year"] = df[column_name].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
        df["release year"] = df["release year"].astype(float)
        return df

    def rename_columns(self, df : pd.DataFrame, column_names=None) -> pd.DataFrame:
        """
        Rename the columns of the dataframe
        """
        if column_names is None:
            column_names = {0: 'Wikipedia movie ID', 1: "Freebase movie ID", 2: "Movie name", 3: "Movie release date",
                            4: "Movie box office revenue", 5: "Movie runtime", 6: "Movie languages",
                            7: "Movie countries", 8: "Movie genres"}
        df.rename(columns=column_names, inplace=True)
        return df

    def add_column(self, df : pd.DataFrame, column_name : str, column_values : list) -> pd.DataFrame:
        """
        Add a column to the dataframe
        """
        df[column_name] = column_values
        return df

    def match_movie_df(self):
        """
        Join two dataframes on a column
        """

        if "Movie runtime" in self.movie_df_sequel_only.columns:
            return


        self.movie_df_sequel_only = self.movie_df_sequel_only.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_books = self.movie_df_books.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_comics = self.movie_df_comics.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_remakes = self.movie_df_remakes.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_sequel_original = self.movie_df_sequel_original.merge(self.movie_df, on="Wikipedia movie ID",how="inner")

    def drop_different_years_df(self, df):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        """
        df["release year wiki"] = df["Movie release date"].apply(
            lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
        df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)

        df.drop(df[df["release year wiki"] != df["release year tmdb"]].index, inplace=True)
        df["release year"] = df["release year wiki"].astype(float)
        df.drop("release year tmdb", axis=1, inplace=True)
        df.drop("release year wiki", axis=1, inplace=True)

        return df

    def drop_different_years(self):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        """
        self.movie_df_sequel_only = self.drop_different_years_df(self.movie_df_sequel_only)
        self.movie_df_books = self.drop_different_years_df(self.movie_df_books)
        self.movie_df_comics = self.drop_different_years_df(self.movie_df_comics)
        self.movie_df_remakes = self.drop_different_years_df(self.movie_df_remakes)
        self.movie_df_sequel_original = self.drop_different_years_df(self.movie_df_sequel_original)


    def get_all_df(self):
        return [self.movie_df, self.movie_df_sequel_only, self.movie_df_books, self.movie_df_comics, self.movie_df_remakes, self.movie_df_sequel_original]

