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
def delete_user(user_db, userdata_db, request):
    yield delete_user
    if hasattr(delete_user, 'username'):
        userdata_db.delete_userdata(delete_user.username)
        user_db.delete_user_authority(delete_user.username)
        user_db.delete_user(delete_user.username)