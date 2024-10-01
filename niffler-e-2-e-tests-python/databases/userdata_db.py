from sqlmodel import Session, select, delete

import allure
from sqlalchemy import create_engine, Engine, event
from allure_commons.types import AttachmentType
from models.userdata import User, Friendship


class UserDataDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)


    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)


    def get_user_profile(self, username):
        with Session(self.engine) as session:
            query = select(User).where(User.username == username)
            return session.exec(query).first()


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
