from fastapi import FastAPI

app = FastAPI(title="FoodieFinder API")

@app.get("/")
def health():
    return {"status": "ok"}