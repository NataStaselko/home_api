from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from app.messages.dependencies import get_messages_service
from app.messages.services import MessageService
from app.messages.schemas import MessagesCreate
from app.messages.models import MessageModel
import redis.asyncio as redis

redis_url = "redis://localhost:6379"

router = APIRouter()


async def get_redis() -> redis.Redis:
    print(redis_url)
    return await redis.from_url(redis_url, decode_responses=True)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_message(
        message: MessagesCreate,
        service: MessageService = Depends(get_messages_service),
        redis: redis.Redis = Depends(get_redis)):

    saved_message = await service.create(**(message.dict()))
    await redis.publish("message_channel", f'{message.text}')
    await redis.publish("chat_channel", f'{message.chat_id}')
    return saved_message



@router.get("", response_model=List[MessageModel])
async def read_messages(
        service: MessageService = Depends(get_messages_service)):
    return await service.list()