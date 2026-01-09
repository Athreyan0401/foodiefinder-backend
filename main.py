from fastapi import FastAPI
from app.core.config import settings
from app.db.database import Base, engine, SessionLocal
from app.routes import auth, reviews, restaurants
from app.db.seed import seed_restaurants

app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)

# 🌱 Seed default restaurants
db = SessionLocal()
seed_restaurants(db)
db.close()

app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(reviews.router)

@app.get("/")
def health():
    return {"status": "FoodieFinder backend running"}