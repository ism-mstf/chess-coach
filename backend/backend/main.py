from fastapi import FastAPI
from .routes import games

app = FastAPI(title="Chess Coach MVP")

app.include_router(games.router, prefix="/api/games")
