from app.database import Database

class RecommenderService:
    @classmethod
    async def get_movies_by_actor(cls, actor_name: str, limit: int = 10):
        """
        Queries MongoDB for movies where the actor is actor_1, actor_2, or actor_3.
        Sorts by imdb_score in descending order and returns the top matches.
        """
        db = Database.get_db()
        movies_collection = db["movies"]
        
        # Build the query
        query = {
            "$or": [
                {"actor_1_name": actor_name},
                {"actor_2_name": actor_name},
                {"actor_3_name": actor_name}
            ]
        }
        
        # Execute query, sort by imdb_score DESC, apply limit
        cursor = movies_collection.find(query).sort("imdb_score", -1).limit(limit)
        
        movies = []
        async for doc in cursor:
            movies.append({
                "title": doc.get("movie_title"),
                "rating": doc.get("imdb_score"),
                "genre": doc.get("genres"),
                "year": doc.get("title_year")
            })
            
        return movies
