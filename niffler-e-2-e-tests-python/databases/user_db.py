from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select

from models.user import User, Authority
from utils.allure_helpers import attach_sql


class UserDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=attach_sql)

    def get_user(self, username: str):
        with Session(self.engine) as session:
            user = select(User).where(User.username == username)
            return (session.exec(user).first())

    def is_user_in_db(self, username: str):
        user_from_db = self.get_user(username)
        if user_from_db.username == username:
            return True
        else:
            print(f'Username: {username} not found')
            return False

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
            if user:
                session.delete(user)
                session.commit()
