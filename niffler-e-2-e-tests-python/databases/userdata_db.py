from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.userdata import User
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

class UserDataDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)


    def delete_userdata(self, username: str):
        with Session(self.engine) as session:
            query = select(User).where(User.username == username)
            user = session.exec(query).one()
            session.delete(user)
            session.commit()
