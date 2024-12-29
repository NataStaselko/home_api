import json
from typing import Any

import asyncio

import redis.asyncio as redis
from redis.exceptions import ResponseError




class RedisClient:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = redis.from_url(self.redis_url)

    async def disconnect(self):
        await self.redis.aclose()


class RedisStreamBase(RedisClient):
    def __init__(self, stream: str, redis_url="redis://localhost:6379", maxlen=1000):
        super().__init__(redis_url)
        self.maxlen = maxlen
        self.stream = stream

    async def count_messages(self):
        count = await self.redis.xlen(self.stream)
        return count

    async def trim_stream(self):
        # Calculate the timestamp for one week ago
        await self.redis.xtrim(self.stream, maxlen=self.maxlen, approximate=False)



class RedisProducerBase(RedisStreamBase):

    async def produce(self, data: dict):
        await self.redis.xadd(self.stream, data)
        await self.trim_stream()