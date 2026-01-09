from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    restaurant_id: str
    content: str
    rating: int = Field(ge=1, le=5)

class ReviewResponse(BaseModel):
    id: str
    restaurant_id: str
    user_id: str
    content: str
    rating: int

    class Config:
        from_attributes = True