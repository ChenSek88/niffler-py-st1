import pytest
from faker import Faker

fake = Faker()


@pytest.fixture()
def user_for_reg():
    username = fake.first_name()
    password = fake.password(length=10)
    yield username, password


@pytest.fixture()
def profile_data():
    name = fake.first_name()
    surname = fake.last_name()
    return name, surname
