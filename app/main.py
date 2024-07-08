from fastapi import FastAPI, Depends, HTTPException, status, File,  UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from app.routers import video
from typing import Annotated
# from transparent_background import Remover
import uvicorn,os

from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Read environment variables
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8000))
print(host,port)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router)

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "This is a service to extract the first frame of a video!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, log_level="info")