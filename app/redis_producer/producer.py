from app.redis_producer.base import RedisProducerBase
from app.core.config import settings
from app.redis_producer.schemas import MessageAddSchema

class MessageProducer(RedisProducerBase):
    def __init__(self):
        super().__init__(
            settings.redis.message_links.stream,
            settings.redis.url,
            maxlen=settings.redis.message_links.maxlen,
        )

    async def add(self, message: MessageAddSchema):
        await self.produce(message.model_dump())


producer_message = MessageProducer()