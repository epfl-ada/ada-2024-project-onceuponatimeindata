from src.data.TMDB_Movies import *
from more_itertools import sliced

def process_movie_data(keywords_name, keywords, start_date="1880-01-01", end_date="2010-01-01"):
    """
    Processes movie data for specified keywords.

    Args:
        keywords_name (list of str): Names of the categories (e.g., "sequels", "book").
        keywords (list of int): IDs corresponding to the keywords in the TMDB database.
        start_date (str): Start date for filtering movies (default is "1880-01-01").
        end_date (str): End date for filtering movies (default is "2010-01-01").

    Returns:
        None. Files are saved to the current directory.
    """
    for i, keyword in enumerate(keywords):
        # Replace `get_data` with the appropriate function call for fetching data
        data = get_data(keywords_name[i], end_date, keyword)  
        file_name = f"{keywords_name[i]}_{start_date[:4]}_{end_date[:4]}.csv"
        data_extended = get_movie_data_extended(data, keywords_name[i])
        get_movie_metadatalike_db(data_extended, keywords_name[i])
        break



def process_sequels_movies(file_paths, years, path="data/sequels"):
    """
    Processes sequel movies by reading CSV files and generating collections.

    Args:
        file_paths (list of str): List of file paths to the sequel movie CSV files.
        years (list of str): Corresponding list of year ranges for each file (e.g., "1880_2010").
        path (str): Base path for storing collection data (default is "data/sequels").

    Returns:
        None. Processes collections and saves results to the specified path.
    """
    for file_path, year_range in zip(file_paths, years):
        sequels_movies = pd.read_csv(file_path)
        get_collection(sequels_movies, path=path, years=year_range)
        break



# Function that adds Wikipedia ID for each movie

def get_wikipedia_id_for_db(df, file):
    """
    Adds a "Wikipedia movie ID" column to a DataFrame and saves it as a CSV.

    Args:
    df (pd.DataFrame): Input DataFrame with movie titles and release dates.
    file (str): Path to save the updated DataFrame as a CSV.

    Returns:
    pd.DataFrame: Updated DataFrame with the "Wikipedia movie ID" column.
    """
    wiki_df = None
    slices = range(0, len(df), 50)  # Creating chunks of 50 rows each
    
    for index in tqdm(slices, total=len(df)//50):
        chunk = df.iloc[index:index+50].copy()
        chunk["Wikipedia movie ID"] = chunk.apply(lambda x: get_wikipedia_id_from_title(x["title"], x["release_date"]), axis=1)
        wiki_df = pd.concat([wiki_df, chunk], axis=0, ignore_index=True, sort=False) if wiki_df is not None else chunk
        wiki_df.to_csv(file, index=False)
        break
    
    return wiki_df



