from app.database import Database
from app.services.similarity import cosine_similarity
import numpy as np

class EmbeddingService:
    # In-memory cache for actor embeddings
    # Format: { "Actor Name": [ [emb1], [emb2], ... ] }
    actor_cache = {}

    @classmethod
    async def load_embeddings(cls):
        """
        Loads all actor embeddings from MongoDB into RAM cache.
        Run this on FastAPI startup.
        """
        db = Database.get_db()
        cursor = db["actor_embeddings"].find({})
        
        cls.actor_cache.clear()
        
        async for doc in cursor:
            actor_name = doc["actor_name"]
            embeddings = doc["embeddings"]
            cls.actor_cache[actor_name] = embeddings
            
        print(f"Loaded {len(cls.actor_cache)} actors into memory.")

    @classmethod
    def recognize_face(cls, query_embedding, threshold=0.35):
        """
        Compares the query embedding against cached actor embeddings.
        Returns the recognized actor name or None if no match is found above the threshold.
        """
        best_match = None
        highest_similarity = -1.0

        if not cls.actor_cache:
            print("WARNING: actor_cache is empty! No embeddings loaded from MongoDB.")
            return None

        for actor_name, embeddings in cls.actor_cache.items():
            max_sim_for_actor = -1.0
            
            for ref_embedding in embeddings:
                sim = cosine_similarity(query_embedding, ref_embedding)
                if sim > max_sim_for_actor:
                    max_sim_for_actor = sim
                    
            if max_sim_for_actor > highest_similarity:
                highest_similarity = max_sim_for_actor
                best_match = actor_name

        print(f"DEBUG - Best match: {best_match} with similarity: {highest_similarity}")

        if highest_similarity >= threshold:
            return best_match
        
        return None
