from pydantic import BaseModel
from typing import Optional

class RestaurantSearchResponse(BaseModel):
    id: str
    name: str
    location: str
    address: Optional[str]
    average_rating: Optional[float]
    review_count: int

    class Config:
        from_attributes = True