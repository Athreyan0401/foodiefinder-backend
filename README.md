# 🍽 FoodieFinder Backend

Community-driven Restaurant Review Application

## 🚀 Features

### Sprint 1

-   User Registration (JWT Based)
-   Secure Login
-   Restaurant Reviews
-   Rating System
-   Edit/Delete Reviews

### Sprint 2

-   Restaurant Search (Name + Location + Address)
-   Photo URL Support
-   Notification System
-   Review Sorting (Newest First)
-   Basic Recommendation Engine
-   Automated Tests

------------------------------------------------------------------------

## 🛠 Tech Stack

-   FastAPI
-   SQLAlchemy ORM
-   PostgreSQL (Neon)
-   JWT Authentication
-   Pytest
-   Render Deployment

------------------------------------------------------------------------

## ▶ Run Server

uvicorn main:app --reload

Swagger Docs: http://localhost:8000/docs

------------------------------------------------------------------------

## 🧪 Run Tests

pytest

------------------------------------------------------------------------

## 🧪 Run Demo Script

python -m scripts.demo_run

------------------------------------------------------------------------

## 🔐 Authentication

Header: Authorization: Bearer `<token>`{=html}

------------------------------------------------------------------------

## 📂 Project Structure

app/ scripts/ tests/

------------------------------------------------------------------------

## 🌍 Deployment

Render + Neon PostgreSQL
