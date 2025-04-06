from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

PORT = config("PORT")

# Create FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Uvicorn!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Points to the "app" instance in the "main" module
        host="0.0.0.0",  # Accessible on your network
        port= int(PORT),       # Port to listen on
        reload=True      # Enable auto-reload for development
    )