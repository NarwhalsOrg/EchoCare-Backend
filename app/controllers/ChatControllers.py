from sqlalchemy.orm import Session
from app.models.ChatHistory import ChatHistory



def create_chat_message(db: Session, user_id: str, session_id: str, message: str, sender: str):
    db_msg = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        message=message,
        sender=sender
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def get_chat_history(db: Session, user_id: str, session_id: str):
    return db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id,
        ChatHistory.session_id == session_id
    ).order_by(ChatHistory.timestamp.asc()).all()