from typing import List
from pydantic import BaseModel, Field

# Using Pydantic models to represent DB documents is good practice

class MovieDB(BaseModel):
    movie_title: str
    actor_1_name: str | None = None
    actor_2_name: str | None = None
    actor_3_name: str | None = None
    genres: str | None = None
    imdb_score: float | None = None
    title_year: int | None = None
    duration: int | None = None
    plot_keywords: str | None = None
    movie_imdb_link: str | None = None

class ActorEmbeddingDB(BaseModel):
    actor_name: str
    embeddings: List[List[float]]
