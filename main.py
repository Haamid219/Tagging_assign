import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import api
from services import load_vector_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    print("Initializing Free Tag Database (HuggingFace)...")
    try:
        api.tag_db = load_vector_db()
        print("System Ready.")
    except Exception as e:
        print(f"Startup Error: {e}")
    yield
    # This runs on shutdown
    print("Shutting down server...")

# Initialize FastAPI with the lifespan handler
app = FastAPI(title="RAG Tagging system", lifespan=lifespan)

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)