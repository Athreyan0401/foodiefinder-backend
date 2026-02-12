from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.auth import get_current_user
from app.models.review import Review
from app.models.notification import Notification
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create review
    review = Review(
        restaurant_id=payload.restaurant_id,
        content=payload.content,
        rating=payload.rating,
        user_id=current_user.id,
        photo_url=payload.photo_url
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    # 🔔 Create notifications for other users
    other_users = (
        db.query(Review.user_id)
        .filter(
            Review.restaurant_id == payload.restaurant_id,
            Review.user_id != current_user.id
        )
        .distinct()
        .all()
    )

    for user in other_users:
        notification = Notification(
            user_id=user[0],
            restaurant_id=payload.restaurant_id,
            review_id=review.id,
            message="New review posted for a restaurant you reviewed."
        )
        db.add(notification)

    db.commit()

    return review


@router.put("/{review_id}")
def update_review(
    review_id: str,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = (
        db.query(Review)
        .filter(
            Review.id == review_id,
            Review.user_id == current_user.id
        )
        .first()
    )

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.content = payload.content
    review.rating = payload.rating
    review.photo_url = payload.photo_url

    db.commit()

    return {"message": "Review updated"}


@router.delete("/{review_id}")
def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = (
        db.query(Review)
        .filter(
            Review.id == review_id,
            Review.user_id == current_user.id
        )
        .first()
    )

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return {"message": "Review deleted"}