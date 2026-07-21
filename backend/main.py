from fastapi import FastAPI

from database import engine
from models import Base


app = FastAPI(
    title="STMA",
    description="Smart Telegram Message Archive",
    version="1.0"
)


# Создание таблиц базы данных
Base.metadata.create_all(
    bind=engine
)


@app.get("/")
def home():

    return {
        "app": "STMA",
        "status": "online",
        "version": "1.0"
    }


@app.get("/health")
def health():

    return {
        "ok": True
    }