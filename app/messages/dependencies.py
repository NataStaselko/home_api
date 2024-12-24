from fastapi import Depends
from app.core.database import database
from app.messages.services import MessageService

async def get_messages_service(
        session: Depends = Depends(database.get_session)) -> MessageService:
    return MessageService(session)

