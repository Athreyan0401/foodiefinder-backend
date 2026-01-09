from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = "FoodieFinder API"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440

settings = Settings()