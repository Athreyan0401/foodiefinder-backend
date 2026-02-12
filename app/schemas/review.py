from pydantic import BaseModel, Field
from typing import Optional
class ReviewCreate(BaseModel):
    restaurant_id: str
    content: str
    rating: int = Field(ge=1, le=5)
    photo_url: Optional[str] = None

class ReviewResponse(BaseModel):
    id: str
    restaurant_id: str
    user_id: str
    content: str
    rating: int
    photo_url: Optional[str]
    
    class Config:
        from_attributes = True