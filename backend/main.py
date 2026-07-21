from fastapi import FastAPI

from database import engine
from models import Base

from api import admin
from api import users
from api import messages


app = FastAPI(
    title="STMA",
    description="Smart Telegram Message Archive",
    version="1.0"
)


# Создание таблиц
Base.metadata.create_all(
    bind=engine
)


# Подключение API
app.include_router(
    admin.router
)

app.include_router(
    users.router
)

app.include_router(
    messages.router
)


@app.get("/")
def home():

    return {
        "app": "STMA",
        "status": "online"
    }


@app.get("/health")
def health():

    return {
        "ok": True
    }