from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from config import ADMIN_TELEGRAM_ID

from models import (
    DisplayStats,
    PremiumPlan,
    PromoCode
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def check_admin(telegram_id: int):

    if telegram_id != ADMIN_TELEGRAM_ID:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


@router.get("/stats")
def stats(
    telegram_id: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    data = db.query(
        DisplayStats
    ).first()

    if not data:
        data = DisplayStats()
        db.add(data)
        db.commit()
        db.refresh(data)

    return data


@router.post("/stats")
def change_stats(
    telegram_id: int,
    users: int,
    messages: int,
    deleted: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    data = db.query(
        DisplayStats
    ).first()

    if not data:
        data = DisplayStats()
        db.add(data)

    data.users_count = users
    data.messages_count = messages
    data.deleted_count = deleted
    data.manual_mode = True

    db.commit()

    return {
        "status": "updated"
    }


@router.post("/premium")
def create_premium_plan(
    telegram_id: int,
    name: str,
    days: int,
    stars: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    plan = PremiumPlan(
        name=name,
        days=days,
        stars_price=stars
    )

    db.add(plan)
    db.commit()

    return {
        "created": True
    }


@router.post("/promo")
def create_promo(
    telegram_id: int,
    code: str,
    days: int,
    uses: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    promo = PromoCode(
        code=code,
        days=days,
        max_uses=uses
    )

    db.add(promo)
    db.commit()

    return {
        "promo": code
    }