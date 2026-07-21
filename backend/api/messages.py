from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Message


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


# Сохранить сообщение
@router.post("/save")
def save_message(
    user_id: int,
    text: str,
    message_type: str = "text",
    db: Session = Depends(get_db)
):

    message = Message(
        user_id=user_id,
        text=text,
        message_type=message_type
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "status": "saved",
        "message_id": message.id
    }


# Получить архив сообщений
@router.get("/{user_id}")
def get_messages(
    user_id: int,
    db: Session = Depends(get_db)
):

    messages = db.query(
        Message
    ).filter(
        Message.user_id == user_id
    ).all()


    return [
        {
            "id": msg.id,
            "text": msg.text,
            "type": msg.message_type,
            "deleted": msg.deleted,
            "date": msg.created_at
        }
        for msg in messages
    ]


# Отметить сообщение удалённым
@router.post("/{message_id}/delete")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):

    message = db.query(
        Message
    ).filter(
        Message.id == message_id
    ).first()


    if not message:
        return {
            "error": "Message not found"
        }


    message.deleted = True

    db.commit()


    return {
        "status": "deleted"
    }