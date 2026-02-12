from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc, asc
from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.core.auth import get_current_user
from app.models.user import User
from app.db.deps import get_db
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.schemas.restaurant import RestaurantSearchResponse


router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/")
def create_restaurant(
    payload: dict,
    db: Session = Depends(get_db)
):
    restaurant = Restaurant(
        name=payload["name"],
        location=payload["location"],
        address=payload.get("address")
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant
@router.get("/")
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()
@router.get("/search", response_model=list[RestaurantSearchResponse])
def search_restaurants(
    query: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=1, le=5),
    sort_by: Optional[str] = Query("rating"),
    order: Optional[str] = Query("desc"),
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Restaurant.id,
            Restaurant.name,
            Restaurant.location,
            func.avg(Review.rating).label("average_rating"),
            func.count(Review.id).label("review_count")
        )
        .outerjoin(Review, Restaurant.id == Review.restaurant_id)
        .group_by(Restaurant.id)
    )
    if query:
        results = results.filter(
            or_(
                Restaurant.name.ilike(f"%{query}%"),
                Restaurant.location.ilike(f"%{query}%")
            )
        )
    if min_rating is not None:
        results = results.having(
            func.avg(Review.rating) >= min_rating
        )
    sort_column = {
        "rating": func.avg(Review.rating),
        "reviews": func.count(Review.id),
        "name": Restaurant.name,
        "newest": Restaurant.created_at
    }.get(sort_by, func.avg(Review.rating))
    if order == "asc":
        results = results.order_by(asc(sort_column))
    else:
        results = results.order_by(desc(sort_column))
    data = results.all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "average_rating": round(r.average_rating, 2) if r.average_rating else None,
            "review_count": r.review_count
        }
        for r in data
    ]

@router.get("/recommendations", response_model=list[RestaurantSearchResponse])
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Step 1: Get restaurants user rated >= 4
    user_reviews = (
        db.query(Review)
        .filter(
            Review.user_id == current_user.id,
            Review.rating >= 4
        )
        .all()
    )

    if user_reviews:
        # Get locations of liked restaurants
        liked_restaurant_ids = [r.restaurant_id for r in user_reviews]

        liked_locations = (
            db.query(Restaurant.location)
            .filter(Restaurant.id.in_(liked_restaurant_ids))
            .distinct()
            .all()
        )

        locations = [loc[0] for loc in liked_locations]

        # Recommend other restaurants in same locations
        results = (
            db.query(
                Restaurant.id,
                Restaurant.name,
                Restaurant.location,
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("review_count")
            )
            .outerjoin(Review, Restaurant.id == Review.restaurant_id)
            .filter(
                Restaurant.location.in_(locations),
                ~Restaurant.id.in_(liked_restaurant_ids)
            )
            .group_by(Restaurant.id)
            .order_by(
                func.avg(Review.rating).desc().nullslast(),
                func.count(Review.id).desc()
            )
            .limit(5)
            .all()
        )
    else:
        # Fallback: Top rated restaurants
        results = (
            db.query(
                Restaurant.id,
                Restaurant.name,
                Restaurant.location,
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("review_count")
            )
            .outerjoin(Review, Restaurant.id == Review.restaurant_id)
            .group_by(Restaurant.id)
            .order_by(
                func.avg(Review.rating).desc().nullslast(),
                func.count(Review.id).desc()
            )
            .limit(5)
            .all()
        )

    return [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "average_rating": round(r.average_rating, 2) if r.average_rating else None,
            "review_count": r.review_count
        }
        for r in results
    ]

@router.get("/{restaurant_id}")
def restaurant_details(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        return {"restaurant": None}

    reviews = (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    avg_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.restaurant_id == restaurant_id)
        .scalar()
    )

    return {
        "restaurant": restaurant,
        "average_rating": round(avg_rating, 2) if avg_rating else None,
        "reviews": reviews
    }