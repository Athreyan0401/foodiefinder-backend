from pydantic import BaseModel

class RestaurantResponse(BaseModel):
    id: str
    name: str
    location: str

    class Config:
        from_attributes = True