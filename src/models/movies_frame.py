import numpy as np
import pandas as pd
from rapidfuzz import fuzz
from plotly import express as px

from utils.data_utils import find_similar_movies
from utils.evaluation_utils import inflate


class MovieFrames:
    """
    Class to handle the dataframes of the movies
    """
    movie_df: pd.DataFrame
    movie_df_sequel_only: pd.DataFrame
    movie_df_books: pd.DataFrame
    movie_df_comics: pd.DataFrame
    movie_df_remakes: pd.DataFrame
    movie_df_sequel_original: pd.DataFrame

    start_year: int
    end_year: int
    old: bool

    def __init__(self, movie_df=None, alternate_df_path=None, start_year=1880, end_year=2010, alternate_df=None):
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

    def add_release_year_df(self, df: pd.DataFrame, column_name: str) -> pd.DataFrame:
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

    def rename_columns(self, df: pd.DataFrame, column_names=None) -> pd.DataFrame:
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

    def add_column(self, df: str, column_name: str, column_values: list):
        """
        add a column to the dataframe
        :param df: the name of the dataframe
        :param column_name: the name of the column
        :param column_values: The values of the column to add
        """
        if df == "Movie":
            self.movie_df[column_name] = column_values
        elif df == "Sequels":
            self.movie_df_sequel_only[column_name] = column_values
        elif df == "Book Adaptation":
            self.movie_df_books[column_name] = column_values
        elif df == "Comics Adaptation":
            self.movie_df_comics[column_name] = column_values
        elif df == "Remake":
            self.movie_df_remakes[column_name] = column_values
        elif df == "Sequels and Original":
            self.movie_df_sequel_original[column_name] = column_values

    def inflate_box_office(self):
        """
        Inflate the box office revenue with the inflation rate
        """
        for df in self.get_all_df(): df["Movie box office revenue inflation adj"] = df.swifter.apply(
            lambda x: inflate(x["Movie box office revenue"], x["release year"]), axis=1)

    def add_missing_values(self, column_name_df, column_name_extended, extended_paths):
        """
        Add the missing values to the dataframes
        :param column_name_df: the name of the column in the dataframe
        :param column_name_extended: the name of the column in the extended dataframe
        :param extended_paths: list of paths to the extended dataframes
        """
        for path in extended_paths:
            extended = pd.read_csv(path, engine = "python")
            for df, name in zip(self.get_all_df(), self.get_all_df_names()):
                added = extended[["id", column_name_extended]]
                added.loc[:, "id"] = pd.to_numeric(added["id"], errors="coerce").astype(float)

                df_new = pd.merge(df, added, on="id", how="inner")
                df_new = df_new[~df_new.duplicated(subset=["id"])]
                df_new_val = self.get_df(name).merge(df_new[["id", column_name_extended]], on="id", how="outer")
                df_new_val[column_name_df] = df_new_val[column_name_df].fillna(df_new_val[column_name_extended])
                self.set_df(name, df_new_val.drop(column_name_extended, axis = 1))

    def get_df(self, df_name):
        """
        Get the dataframe with the name
        :param df_name: the name of the dataframe
        :return: the dataframe
        """
        if df_name == "Movie":
            return self.movie_df
        elif df_name == "Sequels":
            return self.movie_df_sequel_only
        elif df_name == "Book Adaptation":
            return self.movie_df_books
        elif df_name == "Comics Adaptation":
            return self.movie_df_comics
        elif df_name == "Remake":
            return self.movie_df_remakes
        elif df_name == "Sequels and Original":
            return self.movie_df_sequel_original

    def set_df(self, df_name, df):
        """
        Set the dataframe with the name
        :param df_name: the name of the dataframe
        :param df: the dataframe
        """
        if df_name == "Movie":
            self.movie_df = df
        elif df_name == "Sequels":
            self.movie_df_sequel_only = df
        elif df_name == "Book Adaptation":
            self.movie_df_books = df
        elif df_name == "Comics Adaptation":
            self.movie_df_comics = df
        elif df_name == "Remake":
            self.movie_df_remakes = df
        elif df_name == "Sequels and Original":
            self.movie_df_sequel_original = df

    def match_movie_df(self):
        """
        Match the dataframes with the main dataframe selecting the rows with the same wiki movie id
        """

        new_dfs = []
        movies_lost = {}
        all_added = None

        for i, df in enumerate(self.get_all_df()):
            if i == 0:
                continue
            df_new = pd.merge(self.movie_df, df, on="Wikipedia movie ID", how="inner")
            df_missing = df[~df["Wikipedia movie ID"].isin(df_new["Wikipedia movie ID"])]
            """df_similar = find_similar_movies(df_missing, self.movie_df)
            df_missing = df_missing[~df_missing["id"].isin(df_similar["id"])]
            df_new = pd.concat([df_new, df_similar])"""
            new_dfs.append(df_new)
            movies_lost[self.get_all_df_names()[i]] = df_missing
            all_added = df_new if all_added is None else pd.concat([all_added, df_new])

        all_added = all_added.drop_duplicates(subset=["Wikipedia movie ID"])
        self.movie_df = pd.merge(self.movie_df, all_added[["id", "Wikipedia movie ID"]], how="outer")

        self.movie_df_sequel_only = new_dfs[0]
        self.movie_df_books = new_dfs[1]
        self.movie_df_comics = new_dfs[2]
        self.movie_df_remakes = new_dfs[3]
        self.movie_df_sequel_original = new_dfs[4]

        return movies_lost

    def get_color_complementary(self, name):
        """
        Get the color for the plotly graph
        :param name: the name of the dataframe
        """
        colors = px.colors.qualitative.Antique
        if name == "Sequels":
            return colors[0]
        elif name == "Book Adaptation":
            return colors[1]
        elif name == "Comics Adaptation":
            return colors[2]
        elif name == "Remake":
            return colors[8]
        elif name == "Sequels and Original":
            return colors[4]
        elif "all" in name:
            return colors[5]
        return colors[8]

    def get_color_discrete(self, name):
        """
        Get the complementary color for the plotly graph
        :param name: the name of the dataframe
        """
        colors = px.colors.qualitative.Pastel
        if name == "Sequels":
            return colors[0]
        elif name == "Book Adaptation":
            return colors[1]
        elif name == "Comics Adaptation":
            return colors[2]
        elif name == "Remake":
            return colors[3]
        elif name == "Sequels and Original":
            return colors[4]
        elif "all" in name:
            return colors[5]
        return colors[6]

    def drop_different_years_df(self, df):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        :param df: dataframe to drop the rows
        :return: dataframe with the rows dropped
        """

        if not self.old:
            df["release year"] = df["Movie release date"].apply(lambda x: float(str(x)[:4]) if str.isdigit(
                str(x)[:4]) else np.nan) if "Movie release date" in df.columns else df["release year"]
            return df
        df["release year wiki"] = df["Movie release date"].apply(
            lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
        df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)

        df.drop(df[np.abs(np.array(df["release year wiki"]).astype(float) - np.array(df["release year tmdb"]).astype(
            float)) > 1].index, inplace=True)

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
            df.drop(df[df["release year"] >= self.end_year].index, inplace=True)

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

    def drop_too_different_titles_df(self, df):

        titles_given = df["Movie name"]
        titles_tmdb = df["title"]
        titles_tmdb_original = df["original_title"]

        fuzzy_distance = np.array(
            [fuzz.ratio(title_given, title_tmdb) for title_given, title_tmdb in zip(titles_given, titles_tmdb)])
        fuzzy_distance_original = np.array([fuzz.ratio(title_given, title_tmdb) for title_given, title_tmdb in
                                            zip(titles_given, titles_tmdb_original)])
        fuzzy_distance = np.maximum(fuzzy_distance, fuzzy_distance_original)

        df.drop(df[fuzzy_distance < 50].index, inplace=True)

        return df

    def drop_too_different_titles(self):
        """
        Drop rows with too different titles
        """
        self.movie_df_sequel_only = self.drop_too_different_titles_df(self.movie_df_sequel_only)
        self.movie_df_books = self.drop_too_different_titles_df(self.movie_df_books)
        self.movie_df_comics = self.drop_too_different_titles_df(self.movie_df_comics)
        self.movie_df_remakes = self.drop_too_different_titles_df(self.movie_df_remakes)
        self.movie_df_sequel_original = self.drop_too_different_titles_df(self.movie_df_sequel_original)

    def get_all_df(self):
        """
        Get all the dataframes
        :return: list of dataframes
        """
        return [self.movie_df, self.movie_df_sequel_only, self.movie_df_books, self.movie_df_comics,
                self.movie_df_remakes, self.movie_df_sequel_original]

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
        return ["Sequels", "Book Adaptation", "Comics Adaptation", "Remake"]

    def get_all_df_names(self):
        """
        Get the names of the dataframes
        :return: list of strings
        """
        return ["Movie", "Sequels", "Book Adaptation", "Comics Adaptation", "Remake", "Sequels and Original"]

    def read_row_list(self, df_path_list, column_names):
        """
        Read the row list and return the dataframes
        :param df_path_list: list of paths to the dataframes
        :param column_names: the column names to keep
        """
        ratings_df = {}
        for path in df_path_list:
            csv = pd.read_csv(path, engine='python')
            for name in self.get_all_df_names():
                if name.lower().split(" ")[0] in path:
                    ratings_df[name] = csv if name not in ratings_df else pd.concat(
                        [ratings_df[name], csv]).drop_duplicates()
            if "all_sample" in path:
                ratings_df["Movie"] = csv if "Movie" not in ratings_df else pd.concat(
                    [ratings_df["Movie"], csv]).drop_duplicates()

        for name in ratings_df:
            movies = self.get_df(name)
            if column_names in movies.columns:
                continue
            movies["id"] = movies["id"].astype(float)
            ratings = ratings_df[name]
            ratings["id"] = pd.to_numeric(ratings["id"], errors="coerce").astype(float)
            new_df = pd.merge(movies, ratings[["id", column_names]], on="id", how="inner")
            new_df = new_df[
                (~new_df.duplicated(subset=["id"])) | ~new_df.duplicated(subset=["Movie name", "release year"])]
            self.set_df(name, new_df)
