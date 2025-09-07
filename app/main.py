from fastapi import FastAPI
from .database import engine
from .models import Base  # Import from models
from .routers import coffee

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee API", version="1.0.0")

app.include_router(coffee.router)

@app.get("/")
def read_root():
    return {"message" : "Hello Coffee World"}

@app.get("/health")
def health_check():
    return {"status" : "Health OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

