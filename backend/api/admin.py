from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from config import ADMIN_TELEGRAM_ID

from models import DisplayStats, PremiumPlan, PromoCode


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Проверка владельца
def check_admin(telegram_id: int):

    if telegram_id != ADMIN_TELEGRAM_ID:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return True


# Статистика
@router.get("/stats")
def get_stats(
    telegram_id: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    stats = db.query(
        DisplayStats
    ).first()

    if not stats:
        stats = DisplayStats()
        db.add(stats)
        db.commit()
        db.refresh(stats)

    return stats


# Изменить ручные показатели
@router.post("/stats/update")
def update_stats(
    telegram_id: int,
    users: int,
    messages: int,
    deleted: int,
    db: Session = Depends(get_db)
):

    check_admin(telegram_id)

    stats = db.query(
        DisplayStats
    ).first()

    if not stats:
        stats = DisplayStats()
        db.add(stats)

    stats.users_count = users
    stats.messages_count = messages
    stats.deleted_count = deleted
    stats.manual_mode = True

    db.commit()

    return {
        "status": "updated"
    }


# Добавить тариф Premium
@router.post("/premium/add")
def add_plan(
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


# Создать промокод
@router.post("/promo/add")
def add_promo(
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