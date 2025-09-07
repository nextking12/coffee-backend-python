from fastapi import FastAPI
from .database import engine
from .models import Base  # Import from models
from .routers import coffee
from fastapi.middleware.cors import CORSMiddleware


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee API", version="1.0.0")

# Add CORS middleware
# Like @CrossOrigin(origins = "*") in Spring
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coffee.router)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Coffee CRUD API is running!"}

# This runs the app
# Like SpringApplication.run() in Java
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
