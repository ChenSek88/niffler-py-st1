from sqlmodel import SQLModel, Field, MetaData

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
