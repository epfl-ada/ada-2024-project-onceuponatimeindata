import pandas as pd
from src.data.TMDB_Movies import *

def process_movie_data(movie_metadata_path, sequel_collection_path, sequel_with_wiki_id_path, book_with_wiki_id_path, comics_with_wiki_id_path, remake_with_wiki_id_path, output_folder):
    """
    Processes movie metadata and joins with different datasets to generate multiple CSV files.

    Args:
    - movie_metadata_path (str): Path to the movie metadata file (TSV format).
    - sequel_collection_path (str): Path to the sequel collections with Wikipedia IDs.
    - sequel_with_wiki_id_path (str): Path to the sequels dataset with Wikipedia IDs.
    - book_with_wiki_id_path (str): Path to the book adaptations with Wikipedia IDs.
    - comics_with_wiki_id_path (str): Path to the comics adaptations with Wikipedia IDs.
    - remake_with_wiki_id_path (str): Path to the remakes with Wikipedia IDs.
    - output_folder (str): Path to save the output CSV files.

    Returns:
    - None
    """
    
    # Load the movie metadata
    movie_df = pd.read_csv(movie_metadata_path, sep='\t', header=None)
    sequel_collections_with_wiki_id = pd.read_csv(sequel_collection_path)
    
    # Rename columns for better readability
    movie_df.rename(columns={0: 'Wikipedia movie ID', 1: "Freebase movie ID", 2: "Movie name",  3: "Movie release date", 
                             4: "Movie box office revenue", 5: "Movie runtime", 6: "Movie languages", 7: "Movie countries", 
                             8: "Movie genres"}, inplace=True)
    
    # Join movie metadata with sequel collections
    movie_df_sequel_original = movie_df.join(sequel_collections_with_wiki_id.set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_sequel_original.to_csv(f'{output_folder}/movie_df_sequel_original.csv', index=False)
    
    # Join with sequels
    sequels_with_wiki_id = pd.read_csv(sequel_with_wiki_id_path)
    movie_df_sequel_only = movie_df.join(sequels_with_wiki_id.set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_sequel_only.to_csv(f'{output_folder}/movie_df_sequel_only.csv', index=False)
    
    # Join with books
    movie_df_book = movie_df.join(pd.read_csv(book_with_wiki_id_path).set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_book.to_csv(f'{output_folder}/movie_df_book.csv', index=False)
    
    # Join with comics
    movie_df_comics = movie_df.join(pd.read_csv(comics_with_wiki_id_path).set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_comics.to_csv(f'{output_folder}/movie_df_comics.csv', index=False)
    
    # Join with remakes
    movie_df_remake = movie_df.join(pd.read_csv(remake_with_wiki_id_path).set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')
    movie_df_remake.to_csv(f'{output_folder}/movie_df_remake.csv', index=False)