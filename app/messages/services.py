from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_service import BaseService
from app.messages.models import MessageModel
from app.messages.schemas import MessagesCreate

class MessageService(BaseService[MessageModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=MessageModel, session=session)