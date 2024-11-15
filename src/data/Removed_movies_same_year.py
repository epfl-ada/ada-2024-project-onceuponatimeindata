# This file contains the function to remove movies with different release years in the Wikipedia and TMDb datasets

def ensure_same_year(df):
    df["release year wiki"] = df["Movie release date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
    df["release year tmdb"] = df["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
    
    df.drop(df[df["release year wiki"] != df["release year tmdb"]].index, inplace=True)
    df["release year"] = df["release year wiki"].astype(float)
    df.drop("release year tmdb", axis=1, inplace=True)
    df.drop("release year wiki", axis=1, inplace=True)
    
    return df