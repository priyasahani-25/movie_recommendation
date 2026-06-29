from pydantic import BaseModel
from typing import List

class HealthResponse(BaseModel):
    status: str

class MovieResponse(BaseModel):
    title: str
    rating: float | None
    genre: str | None
    year: int | None

class PredictResponse(BaseModel):
    actor: str
    movies: List[MovieResponse]
