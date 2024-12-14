import numpy as np
import pandas as pd
from future.backports.http.cookiejar import unmatched


class MovieFrames:
    """
    Class to handle the dataframes of the movies
    """
    movie_df : pd.DataFrame
    movie_df_sequel_only : pd.DataFrame
    movie_df_books : pd.DataFrame
    movie_df_comics : pd.DataFrame
    movie_df_remakes : pd.DataFrame
    movie_df_sequel_original : pd.DataFrame

    start_year : int
    end_year : int
    old : bool

    def __init__(self, movie_df=None, alternate_df_path=None, start_year = 1880, end_year = 2010, alternate_df=None):
        """
        Initialize the class
        :param movie_df: path to the main dataframe provided by the course
        :param alternate_df_path: list of path to the alternate dataframes
        :param start_year: start year of the analysis
        :param end_year: end year of the analysis
        :param alternate_df: list of dataframes
        """

        self.start_year = start_year
        self.end_year = end_year
        self.old = end_year <= 2010

        if alternate_df is not None:
            self.movie_df = alternate_df[0]
            self.movie_df_sequel_only = alternate_df[1]
            self.movie_df_books = alternate_df[2]
            self.movie_df_comics = alternate_df[3]
            self.movie_df_remakes = alternate_df[4]
            self.movie_df_sequel_original = alternate_df[5]
            return

        self.movie_df = movie_df

        for df in alternate_df_path:
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
        :return: None
        """

        self.movie_df = self.add_release_year_df(self.movie_df, "Movie release date")
        self.movie_df_sequel_only = self.add_release_year_df(self.movie_df_sequel_only, "Movie release date")
        self.movie_df_books = self.add_release_year_df(self.movie_df_books, "Movie release date")
        self.movie_df_comics = self.add_release_year_df(self.movie_df_comics, "Movie release date")
        self.movie_df_remakes = self.add_release_year_df(self.movie_df_remakes, "Movie release date")
        self.movie_df_sequel_original = self.add_release_year_df(self.movie_df_sequel_original, "Movie release date")


    def concat_movie_frame(self, other_mf):
        """
        Concatenate a MovieFrames object to the current object
        :param other_mf: the other MovieFrames object
        :param column_names: the new names of the columns
        """

        start_year = other_mf.start_year if other_mf.start_year < self.start_year else self.start_year
        end_year = other_mf.end_year if other_mf.end_year > self.end_year else self.end_year

        new_dfs = []
        for df, df_other in zip(self.get_all_df(), other_mf.get_all_df()):
            df_other["Movie box office revenue"] = np.array(df_other["Movie box office revenue"]).astype(float)
            df_other["Movie runtime"] = np.array(df_other["Movie runtime"]).astype(float)
            new_dfs.append(pd.concat([df, df_other]))


        return MovieFrames(alternate_df=new_dfs,
                           start_year=start_year, end_year=end_year)

    def add_release_year_df(self, df : pd.DataFrame, column_name : str) -> pd.DataFrame:
        """
        Add a column with the release year to the dataframe

        :param df: dataframe to add the column
        :param column_name: column with the release date
        :return: dataframe with the release year
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
        :param df: dataframe to rename the columns
        :param column_names: The new names of the columns
        :return: the dataframe with the new column names
        """
        if column_names is None:
            column_names = {0: 'Wikipedia movie ID', 1: "Freebase movie ID", 2: "Movie name", 3: "Movie release date",
                            4: "Movie box office revenue", 5: "Movie runtime", 6: "Movie languages",
                            7: "Movie countries", 8: "Movie genres"}
        df.rename(columns=column_names, inplace=True)
        return df

    def add_column(self, df : str, column_name : str, column_values : list):
        """
        add a column to the dataframe
        :param df: the name of the dataframe
        :param column_name: the name of the column
        :param column_values: The values of the column to add
        """
        if df == "movie_df":
            self.movie_df[column_name] = column_values
        elif df == "movie_df_sequel_only":
            self.movie_df_sequel_only[column_name] = column_values
        elif df == "movie_df_books":
            self.movie_df_books[column_name] = column_values
        elif df == "movie_df_comics":
            self.movie_df_comics[column_name] = column_values
        elif df == "movie_df_remakes":
            self.movie_df_remakes[column_name] = column_values
        elif df == "movie_df_sequel_original":
            self.movie_df_sequel_original[column_name] = column_values

    def match_movie_df(self):
        """
        Match the dataframes with the main dataframe
        """

        test = self.movie_df_sequel_only
        self.movie_df_sequel_only = self.movie_df_sequel_only[["Wikipedia movie ID", "release_date"]].merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        unmatched = test[~test["Wikipedia movie ID"].isin(self.movie_df_sequel_only["Wikipedia movie ID"])]

        test = self.movie_df_books
        self.movie_df_books = self.movie_df_books[["Wikipedia movie ID", "release_date"]].merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        unmatched = test[~test["Wikipedia movie ID"].isin(self.movie_df_books["Wikipedia movie ID"])]

        self.movie_df_comics = self.movie_df_comics[["Wikipedia movie ID", "release_date"]].merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_remakes = self.movie_df_remakes[["Wikipedia movie ID", "release_date"]].merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_sequel_original = self.movie_df_sequel_original[["Wikipedia movie ID", "release_date"]].merge(self.movie_df, on="Wikipedia movie ID",how="inner")

    def drop_different_years_df(self, df):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        :param df: dataframe to drop the rows
        :return: dataframe with the rows dropped
        """
        if not self.old:
            df["release year"] = df["Movie release date"].apply(lambda x: float(str(x)[:4]) if str.isdigit(str(x)[:4]) else np.nan)
            return df
        df["release year wiki"] = df["Movie release date"].apply(
            lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
        df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)

        df.drop(df[np.abs(np.array(df["release year wiki"]).astype(float) - np.array(df["release year tmdb"]).astype(float)) > 1].index, inplace=True)

        df["release year"] = df["release year wiki"].astype(float)
        df.drop("release year tmdb", axis=1, inplace=True)
        df.drop("release year wiki", axis=1, inplace=True)

        return df

    def drop_impossible_years(self):
        """
        Drop rows with impossible release years
        """

        for df in self.get_all_df():
            df.drop(df[df["release year"] < self.start_year].index, inplace=True)
            df.drop(df[df["release year"] > self.end_year].index, inplace=True)


    def drop_different_years(self):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        """
        self.movie_df["release year"] = self.movie_df["Movie release date"].apply(
            lambda x: float(str(x)[:4]) if str.isdigit(str(x)[:4]) else np.nan)
        self.movie_df_sequel_only = self.drop_different_years_df(self.movie_df_sequel_only)
        self.movie_df_books = self.drop_different_years_df(self.movie_df_books)
        self.movie_df_comics = self.drop_different_years_df(self.movie_df_comics)
        self.movie_df_remakes = self.drop_different_years_df(self.movie_df_remakes)
        self.movie_df_sequel_original = self.drop_different_years_df(self.movie_df_sequel_original)


    def get_all_df(self):
        """
        Get all the dataframes
        :return: list of dataframes
        """
        return [self.movie_df, self.movie_df_sequel_only, self.movie_df_books, self.movie_df_comics, self.movie_df_remakes, self.movie_df_sequel_original]

    def get_all_alternate_df(self):
        """
        Get all the alternate dataframes
        :return: list of dataframes
        """
        return [self.movie_df_sequel_only, self.movie_df_books, self.movie_df_comics, self.movie_df_remakes]

    def get_all_alternate_df_names(self):
        """
        Get the names of the alternate dataframes
        :return: list of strings
        """
        return ["Sequels", "Books", "Comics", "Remakes"]