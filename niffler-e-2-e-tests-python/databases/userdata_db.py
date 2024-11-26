from sqlmodel import Session, select, delete

from sqlalchemy import create_engine, Engine, event
from models.userdata import User, Friendship
from utils.allure_helpers import attach_sql


class UserDataDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        event.listen(self.engine, "do_execute", fn=attach_sql)

    def get_user_profile(self, username):
        with Session(self.engine) as session:
            query = select(User).where(User.username == username)
            return session.exec(query).first()

    def firstname_surname_in_db(self, username):
        profile_from_db = self.get_user_profile(username)
        if profile_from_db:
            return profile_from_db.firstname, profile_from_db.surname
        else:
            print(f'Profile for: {username} not found')
            return False

    def delete_userdata(self, username: str):
        with Session(self.engine) as session:
            query = select(User).where(User.username == username)
            user = session.exec(query).one()
            session.delete(user)
            session.commit()

    def delete_friend(self, username: str):
        # Чтобы полностью удалить запись в таблице friendship между друзьями, необходимо удалить две записи
        # В одной записи id юзера будет в качестве addressee_id, а в другой в качестве requester_id
        addressee = delete(Friendship).where(Friendship.addressee_id == (select(User.id).where(User.username == username)).scalar_subquery())
        requester = delete(Friendship).where(Friendship.requester_id == (select(User.id).where(User.username == username)).scalar_subquery())
        with Session(self.engine) as session:
            session.exec(addressee)
            session.exec(requester)
            session.commit()
