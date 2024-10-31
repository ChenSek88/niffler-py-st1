import pytest
from faker import Faker

fake = Faker()


@pytest.fixture()
def user_for_reg(user_db, userdata_db, is_user_in_db):
    username = fake.first_name()
    password = fake.password(length=10)
    yield username, password


@pytest.fixture()
def profile_data():
    name = fake.first_name()
    surname = fake.last_name()
    return name, surname
