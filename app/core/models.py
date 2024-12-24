from sqlmodel import Field, SQLModel
from sqlalchemy import Column, BigInteger

class IDModel(SQLModel):
    id: int = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    )