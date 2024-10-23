import pytest
from faker import Faker

fake = Faker()


@pytest.fixture()
def user_for_reg(user_db, userdata_db, user_in_db):
    username = fake.first_name()
    password = fake.password(length=10)
    yield username, password
    if user_in_db(username) == username:
        userdata_db.delete_userdata(username)
        user_db.delete_user_authority(username)
        user_db.delete_user(username)


@pytest.fixture()
def profile_data():
    name = fake.first_name()
    surname = fake.last_name()
    return name, surname