from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select, delete

from models.userdata import User, Friendship


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


    def delete_friend_request(self, username: str):
        query = delete(Friendship).where(Friendship.addressee_id == (select(User.id).where(User.username == username)).scalar_subquery())
        query2 = delete(Friendship).where(Friendship.requester_id == (select(User.id).where(User.username == username)).scalar_subquery())
        with Session(self.engine) as session:
            session.exec(query)
            session.exec(query2)
            session.commit()
