from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)

from datetime import datetime

from database import Base


# Пользователи STMA
class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    telegram_id = Column(
        String,
        unique=True,
        index=True
    )

    username = Column(
        String,
        nullable=True
    )

    premium = Column(
        Boolean,
        default=False
    )

    premium_expires_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# Сообщения
class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    text = Column(
        Text
    )

    message_type = Column(
        String,
        default="text"
    )

    deleted = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# Premium тарифы
class PremiumPlan(Base):

    __tablename__ = "premium_plans"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String
    )

    days = Column(
        Integer
    )

    stars_price = Column(
        Integer
    )

    active = Column(
        Boolean,
        default=True
    )


# Промокоды
class PromoCode(Base):

    __tablename__ = "promo_codes"

    id = Column(
        Integer,
        primary_key=True
    )

    code = Column(
        String,
        unique=True
    )

    days = Column(
        Integer
    )

    max_uses = Column(
        Integer,
        default=1
    )

    used_count = Column(
        Integer,
        default=0
    )

    active = Column(
        Boolean,
        default=True
    )


# История оплат Stars
class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer
    )

    stars_amount = Column(
        Integer
    )

    plan_days = Column(
        Integer
    )

    status = Column(
        String,
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# Настройки отображаемой статистики
class DisplayStats(Base):

    __tablename__ = "display_stats"

    id = Column(
        Integer,
        primary_key=True
    )

    manual_mode = Column(
        Boolean,
        default=False
    )

    users_count = Column(
        Integer,
        default=0
    )

    messages_count = Column(
        Integer,
        default=0
    )

    deleted_count = Column(
        Integer,
        default=0
    )

    storage_size = Column(
        String,
        default="0 GB"
    )