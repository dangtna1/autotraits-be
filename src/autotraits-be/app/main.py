from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import plants, auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(plants.router, prefix="/api", tags=["Plant API"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For public access, or specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
