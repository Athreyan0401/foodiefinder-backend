from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant

DEFAULT_RESTAURANTS = [
    {
        "name": "Master Cafe",
        "location": "Chennai",
        "address": "123 Anna Salai, Chennai"
    },
    {
        "name": "Kaithi Biryani",
        "location": "Chennai",
        "address": "45 Mount Road, Chennai"
    },
    {
        "name": "Jigarthanda Junction",
        "location": "Madurai",
        "address": "12 Town Hall Road, Madurai"
    }
]
def seed_restaurants(db: Session):
    existing_count = db.query(Restaurant).count()
    if existing_count > 0:
        return

    restaurants = [Restaurant(**data) for data in DEFAULT_RESTAURANTS]
    db.add_all(restaurants)
    db.commit()