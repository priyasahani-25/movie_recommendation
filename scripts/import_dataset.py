import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import get_sync_db
import math

def import_data():
    dataset_path = "dataset/movie_metadata.csv"
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found. Please place the CSV file in the dataset directory.")
        return

    print(f"Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Keep only required columns
    required_columns = [
        "movie_title", "actor_1_name", "actor_2_name", "actor_3_name",
        "genres", "imdb_score", "title_year", "duration",
        "plot_keywords", "movie_imdb_link"
    ]
    
    # Check if all required columns exist
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns in dataset: {missing_cols}")
        return

    df = df[required_columns]

    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=["movie_title", "title_year"])
    print(f"Removed {initial_count - len(df)} duplicates.")

    # Handle missing values
    # For strings, fill with empty string. For numbers, drop or fill with 0/None.
    # We will drop rows where movie_title or imdb_score is missing
    df = df.dropna(subset=["movie_title", "imdb_score"])
    
    # Fill remaining NaNs appropriately
    df["actor_1_name"] = df["actor_1_name"].fillna("")
    df["actor_2_name"] = df["actor_2_name"].fillna("")
    df["actor_3_name"] = df["actor_3_name"].fillna("")
    df["genres"] = df["genres"].fillna("")
    df["plot_keywords"] = df["plot_keywords"].fillna("")
    df["movie_imdb_link"] = df["movie_imdb_link"].fillna("")
    
    # For numerical columns, replace NaN with 0 or -1 (or drop, depending on requirements, let's fill with 0)
    df["title_year"] = df["title_year"].fillna(0).astype(int)
    df["duration"] = df["duration"].fillna(0).astype(int)

    # Clean movie_title (often has trailing spaces or weird characters in some datasets)
    df["movie_title"] = df["movie_title"].str.strip()

    # Convert DataFrame to list of dictionaries
    movies = df.to_dict(orient="records")

    print(f"Prepared {len(movies)} movies for insertion.")

    # Get synchronous DB client
    db = get_sync_db()
    movies_collection = db["movies"]

    # Clear existing data (optional, but good for idempotency)
    movies_collection.delete_many({})
    print("Cleared existing movies collection.")

    # Insert into MongoDB
    if movies:
        result = movies_collection.insert_many(movies)
        print(f"Successfully inserted {len(result.inserted_ids)} movies into MongoDB.")
    else:
        print("No movies to insert.")

if __name__ == "__main__":
    import_data()
