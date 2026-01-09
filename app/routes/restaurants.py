from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db
from app.models.restaurant import Restaurant
from app.models.review import Review

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()

@router.get("/{restaurant_id}")
def restaurant_details(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.restaurant_id == restaurant_id
    ).scalar()

    return {
        "restaurant": restaurant,
        "average_rating": round(avg_rating, 2) if avg_rating else None
    }