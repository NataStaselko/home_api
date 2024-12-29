from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from app.messages.dependencies import get_messages_service
from app.messages.services import MessageService
from app.messages.schemas import MessagesCreate
from app.messages.models import MessageModel
from app.redis_producer.producer import producer_message
from app.redis_producer.schemas import MessageAddSchema


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_message(
        message: MessagesCreate,
        service: MessageService = Depends(get_messages_service)):
    message_schema  = MessageAddSchema(
        message_id=message.message_id,
        from_user_id=message.from_user_id,
        chat_id=message.chat_id,
        text=message.text)
    await producer_message.add(message_schema)

    saved_message = await service.create(**(message.dict()))

    return saved_message



@router.get("", response_model=List[MessageModel])
async def read_messages(
        service: MessageService = Depends(get_messages_service)):
    return await service.list()