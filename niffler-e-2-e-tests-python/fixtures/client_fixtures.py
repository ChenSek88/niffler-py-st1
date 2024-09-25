import pytest

from clients.friends_client import FriendsHttpClient
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs
from databases.user_db import UserDb
from databases.userdata_db import UserDataDb


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


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
def friends_client(envs, auth_token) -> FriendsHttpClient:
    return FriendsHttpClient(envs, auth_token)