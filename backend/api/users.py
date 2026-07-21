from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register_user(
    telegram_id: str,
    username: str = None,
    db: Session = Depends(get_db)
):

    user = db.query(
        User
    ).filter(
        User.telegram_id == telegram_id
    ).first()


    if user:

        return {
            "status": "exists",
            "user_id": user.id
        }


    new_user = User(
        telegram_id=telegram_id,
        username=username
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "status": "created",
        "user_id": new_user.id
    }


@router.get("/{telegram_id}")
def get_user(
    telegram_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(
        User
    ).filter(
        User.telegram_id == telegram_id
    ).first()


    if not user:

        return {
            "error": "User not found"
        }


    return {
        "id": user.id,
        "username": user.username,
        "premium": user.premium,
        "premium_expires": user.premium_expires_at
    }