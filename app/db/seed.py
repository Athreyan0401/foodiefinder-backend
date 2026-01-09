from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant

DEFAULT_RESTAURANTS = [
    {"name": "Kaithi Biryani", "location": "Chennai"},
    {"name": "Master Cafe", "location": "Chennai"},
    {"name": "Baasha Mess", "location": "Chennai"},
    {"name": "Vikram Kitchen", "location": "Chennai"},
    {"name": "Thalapathi Darbar", "location": "Madurai"},
    {"name": "Jigarthanda Junction", "location": "Madurai"},
]

def seed_restaurants(db: Session):
    existing_count = db.query(Restaurant).count()
    if existing_count > 0:
        return  # ✅ already seeded

    restaurants = [Restaurant(**data) for data in DEFAULT_RESTAURANTS]
    db.add_all(restaurants)
    db.commit()