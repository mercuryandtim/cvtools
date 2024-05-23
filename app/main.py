from fastapi import FastAPI, Depends, HTTPException, status, File,  UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from .routers import video
from typing import Annotated
# from transparent_background import Remover


from datetime import timedelta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(video.router)
