import numpy as np
import pandas as pd


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

    def __init__(self, movie_df, alternate_df : list, start_year, end_year):
        """
        Initialize the class
        :param movie_df: path to the main dataframe provided by the course
        :param alternate_df: list of path to the alternate dataframes
        :param start_year: start year of the analysis
        :param end_year: end year of the analysis
        """

        self.movie_df = movie_df
        self.movie_df = self.extract_country_genre(self.movie_df)
        self.start_year = start_year
        self.end_year = end_year
        self.old = end_year <= 2010

        for df in alternate_df:
            if "book" in df:
                self.movie_df_books = pd.read_csv(df)
                self.movie_df_books = self.extract_country_genre(self.movie_df_books)
                
            elif "comics" in df:
                self.movie_df_comics = pd.read_csv(df)
                self.movie_df_comics = self.extract_country_genre(self.movie_df_comics)
            elif "remake" in df:
                self.movie_df_remakes = pd.read_csv(df)
                self.movie_df_remakes = self.extract_country_genre(self.movie_df_remakes)
                
            elif "sequel" in df and "original" in df:
                self.movie_df_sequel_original = pd.read_csv(df)
                self.movie_df_sequel_original = self.extract_country_genre(self.movie_df_sequel_original)
                
            elif "sequel" in df:
                self.movie_df_sequel_only = pd.read_csv(df)
                self.movie_df_sequel_only = self.extract_country_genre(self.movie_df_sequel_only)
                
        



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
        """
        if "Movie runtime" in self.movie_df_sequel_only.columns:
            return"""


        self.movie_df_sequel_only = self.movie_df_sequel_only.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_books = self.movie_df_books.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_comics = self.movie_df_comics.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_remakes = self.movie_df_remakes.merge(self.movie_df, on="Wikipedia movie ID", how="inner")
        self.movie_df_sequel_original = self.movie_df_sequel_original.merge(self.movie_df, on="Wikipedia movie ID",how="inner")

    def drop_different_years_df(self, df):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        :param df: dataframe to drop the rows
        :return: dataframe with the rows dropped
        """
        df["release year wiki"] = df["Movie release date"].apply(
            lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
        df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)

        df.drop(df[df["release year wiki"] != df["release year tmdb"]].index, inplace=True)
        df["release year"] = df["release year wiki"].astype(float)
        df.drop("release year tmdb", axis=1, inplace=True)
        df.drop("release year wiki", axis=1, inplace=True)

        return df

    def drop_impossible_years(self):
        """
        Drop rows with impossible release years
        """
        self.movie_df = self.movie_df[self.movie_df["release year"] > 1880]
        self.movie_df_sequel_only = self.movie_df_sequel_only[self.movie_df_sequel_only["release year"] > 1880]
        self.movie_df_books = self.movie_df_books[self.movie_df_books["release year"] > 1880]
        self.movie_df_comics = self.movie_df_comics[self.movie_df_comics["release year"] > 1880]
        self.movie_df_remakes = self.movie_df_remakes[self.movie_df_remakes["release year"] > 1880]
        self.movie_df_sequel_original = self.movie_df_sequel_original[self.movie_df_sequel_original["release year"] > 1880]

    def drop_different_years(self):
        """
        Drop rows with different release years between the Wikipedia and TMDb datasets
        """
        self.movie_df_sequel_only = self.drop_different_years_df(self.movie_df_sequel_only)
        self.movie_df_books = self.drop_different_years_df(self.movie_df_books)
        self.movie_df_comics = self.drop_different_years_df(self.movie_df_comics)
        self.movie_df_remakes = self.drop_different_years_df(self.movie_df_remakes)
        self.movie_df_sequel_original = self.drop_different_years_df(self.movie_df_sequel_original)



    def extract_country_genre(self,df):
        """
        Extract the country from the country column
        """
        
        if "Movie countries"  in df.columns and "Movie genres"  in df.columns:
            

            df['Movie countries'] = df['Movie countries'].str.extract(r"'name': '([^']+)'.*")
            
            
            genre_regex = r"'name': '([^']+)'"
            df["Genres List"] = df["Movie genres"].str.findall(genre_regex)

            max_genres = df["Genres List"].apply(len).max()
            for i in range(max_genres):
                df[f"Genre {i+1}"] = df["Genres List"].apply(lambda x: x[i] if i < len(x) else None)
            
            df.drop(columns=["Genres List"], inplace=True)



        return df
       

    def get_all_df(self):
        """
        Get all the dataframes
        :return: list of dataframes
        """
        return [self.movie_df, self.movie_df_sequel_only, self.movie_df_books, self.movie_df_comics, self.movie_df_remakes, self.movie_df_sequel_original]


