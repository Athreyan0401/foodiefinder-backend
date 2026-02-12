import json
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.models.notification import Notification
from app.core.security import hash_password, create_access_token


def pretty(data):
    print(json.dumps(data, indent=2, default=str))


def run_demo():
    db: Session = SessionLocal()

    output = {}

    user_a = db.query(User).filter_by(email="demo_user_a@example.com").first()
    if not user_a:
        user_a = User(
            email="demo_user_a@example.com",
            password_hash=hash_password("password123")
        )
        db.add(user_a)
        db.commit()
        db.refresh(user_a)

    user_b = db.query(User).filter_by(email="demo_user_b@example.com").first()
    if not user_b:
        user_b = User(
            email="demo_user_b@example.com",
            password_hash=hash_password("password123")
        )
        db.add(user_b)
        db.commit()
        db.refresh(user_b)

    output["users_created"] = [
        {"id": user_a.id, "email": user_a.email},
        {"id": user_b.id, "email": user_b.email},
    ]

    # ---------- Generate Tokens ----------
    token_a = create_access_token({"sub": user_a.id})
    token_b = create_access_token({"sub": user_b.id})

    output["tokens"] = {
        "user_a_token": token_a,
        "user_b_token": token_b
    }

    # ---------- Pick a Restaurant ----------
    restaurant = db.query(Restaurant).first()

    output["restaurant_selected"] = {
        "id": restaurant.id,
        "name": restaurant.name,
        "location": restaurant.location,
        "address": restaurant.address
    }

    # ---------- User A posts review ----------
    review_a = Review(
        restaurant_id=restaurant.id,
        user_id=user_a.id,
        content="Amazing food!",
        rating=5,
        photo_url=None
    )

    db.add(review_a)
    db.commit()
    db.refresh(review_a)

    # ---------- User B posts review (triggers notification) ----------
    review_b = Review(
        restaurant_id=restaurant.id,
        user_id=user_b.id,
        content="Nice ambience.",
        rating=4,
        photo_url=None
    )

    db.add(review_b)
    db.commit()
    db.refresh(review_b)

    # Trigger notification manually (same logic as route)
    notification = Notification(
        user_id=user_a.id,
        restaurant_id=restaurant.id,
        review_id=review_b.id,
        message="New review posted for a restaurant you reviewed."
    )

    db.add(notification)
    db.commit()

    output["reviews_posted"] = [
        {"id": review_a.id, "user": "A", "rating": 5},
        {"id": review_b.id, "user": "B", "rating": 4},
    ]

    # ---------- Fetch Notifications ----------
    notifications = db.query(Notification).filter(
        Notification.user_id == user_a.id
    ).all()

    output["notifications_for_user_a"] = [
        {
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ]

    # ---------- Recommendations ----------
    recommendations = db.query(Restaurant).limit(3).all()

    output["recommendations_sample"] = [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location
        }
        for r in recommendations
    ]

    pretty(output)
    db.close()


if __name__ == "__main__":
    run_demo()