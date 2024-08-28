from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.user import User, Authority


class UserDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)


    def delete_user_authority(self, username: str):
        with Session(self.engine) as session:
            query = select(User.id).where(User.username == username)
            user_id = session.exec(query).first()

            query2 = select(Authority.id).where(Authority.user_id == user_id)
            authority_ids = [r for r in session.exec(query2)]
            for authority in authority_ids:
                user_authority = session.get(Authority, authority)
                session.delete(user_authority)
            session.commit()


    def delete_user(self, username: str):
        with Session(self.engine) as session:
            query = select(User.id).where(User.username == username)
            user_id = session.exec(query).first()
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
