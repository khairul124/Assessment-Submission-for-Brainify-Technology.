from pydantic import BaseModel
from datetime import date


class Product(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    id: str
    name: str
    url: str
    installs: int
    rating: float
    review_count: int
    last_updated: date
    category: str = "unknown"
    score: float = 0.0