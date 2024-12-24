from sqlmodel import Field, SQLModel
from sqlalchemy import Column, BigInteger, Text
from app.core.models import IDModel


class MessageModel(IDModel, table=True):
    __tablename__ = "messages"

    message_id: int = Field(
        description="Unique message identifier inside this chat.",
        sa_column=Column(BigInteger(), nullable=False),
    )
    from_user_id: int = Field(
        description="Sender of the message.",
        sa_column=Column(BigInteger(), nullable=False),
    )
    chat_id: int = Field(
        description="Conversation the message belongs to.",
        sa_column=Column(BigInteger(), nullable=False),
    )
    text: str = Field(
        description="The actual UTF-8 text of the message.",
        max_length=4096,
        sa_column=Column(Text, nullable=False),
    )
    date: int = Field(description="Date the message was sent in Unix time.")
    response_score: int | None = Field(
        default=None,
        description="The score of the bot's response, can be either 1 or 0.",
    )
    feedback: str = Field(
        description="User's feedback or review.",
        max_length=4096,
        sa_column=Column(Text, nullable=True),
    )
