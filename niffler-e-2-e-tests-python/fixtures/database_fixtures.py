import pytest

from databases.spend_db import SpendDb
from databases.user_db import UserDb
from databases.userdata_db import UserDataDb


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def user_db(envs) -> UserDb:
    return UserDb(envs.user_db_url)


@pytest.fixture(scope="session")
def userdata_db(envs) -> UserDataDb:
    return UserDataDb(envs.userdata_db_url)


@pytest.fixture()
def is_user_in_db(user_db):
    def get_username_from_db(username: str):
        user = user_db.get_user(username)
        return user.username if user else print(f'Username: {username} not found')
    return get_username_from_db


@pytest.fixture()
def is_category_in_db(spend_db):
    def get_category_from_db(category_name):
        category = spend_db.get_category(category_name)
        return category.category if category else print(f'Category: {category_name} not found')
    return get_category_from_db


@pytest.fixture()
def is_firstname_surname_in_db(userdata_db):
    def get_firstname_surname_from_db(username):
        user_profile = userdata_db.get_user_profile(username)
        return user_profile.firstname, user_profile.surname
    return get_firstname_surname_from_db


@pytest.fixture()
def delete_user(user_db, userdata_db, is_user_in_db, request):
    username = None

    def set_username(user):
        nonlocal username
        username = user

    request.param = set_username
    yield set_username
    if username and is_user_in_db(username) == username:
        userdata_db.delete_userdata(username)
        user_db.delete_user_authority(username)
        user_db.delete_user(username)