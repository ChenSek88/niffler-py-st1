from sqlmodel import SQLModel, Field, MetaData

metadata = MetaData()

class User(SQLModel, table=True):
    metadata = metadata
    id: str = Field(default=None, primary_key=True)
    username: str
    password: str
    enabled: bool
    account_non_expired: bool
    account_non_locked: bool
    credentials_non_expired: bool


class Authority(SQLModel, table=True):
    metadata = metadata
    id: str = Field(default=None, primary_key=True)
    user_id: str
    authority: str
