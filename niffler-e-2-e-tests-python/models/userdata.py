from sqlmodel import SQLModel, Field, MetaData
from datetime import datetime


metadata2 = MetaData()

class User(SQLModel, table=True):
    metadata = metadata2
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str
    firstname: str
    surname: str
    photo: bytes
    photo_small: bytes


class Friendship(SQLModel, table=True):
    requester_id: str = Field(default=None, primary_key=True)
    addressee_id: str
    status: str
    created_date: datetime