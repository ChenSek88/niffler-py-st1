import pytest
from _pytest.fixtures import FixtureRequest

from clients.friends_client import FriendsHttpClient
from clients.registration_client import UserRegistrationHTTPClient
from clients.spends_client import SpendsHttpClient
from clients.userdata_client import UserdataHttpClient
from models.enums import Category
from models.config import Envs


@pytest.fixture(scope="session")
def registration_client(envs: Envs, user_db, userdata_db) -> UserRegistrationHTTPClient:
    client = UserRegistrationHTTPClient(envs)
    yield client
    if hasattr(client, 'username'):
        userdata_db.delete_userdata(client.username)
        user_db.delete_user_authority(client.username)
        user_db.delete_user(client.username)


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


@pytest.fixture(scope="session")
def userdata_client(envs: Envs, auth_token) -> UserdataHttpClient:
    return UserdataHttpClient(envs, auth_token)


@pytest.fixture(scope="session")
def friends_client(envs: Envs, auth_token) -> FriendsHttpClient:
    return FriendsHttpClient(envs, auth_token)


@pytest.fixture(params=[])
def category(request: FixtureRequest, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.json()['category']
    spend_db.delete_category(category.json()['id'])


@pytest.fixture()
def remove_all_categories(request: FixtureRequest, spends_client, spend_db):
    yield
    categories = spends_client.get_categories()
    [spend_db.delete_category(category['id']) for category in categories.json() if category]


@pytest.fixture(params=[])
def spends(request, spends_client):
    spends_client.add_spends(request.param)
    yield
    spends = spends_client.get_spends()
    [spends_client.remove_spends(spend['id']) for spend in spends.json() if spend]


@pytest.fixture()
def remove_all_spends(request: FixtureRequest, spends_client):
    yield
    all_spends = spends_client.get_spends()
    [spends_client.remove_spends(spend['id']) for spend in all_spends.json() if spend]


CATEGORIES = [
    Category.SCHOOL,
    Category.INTERNET,
    Category.CARSHARING,
    Category.PHARMACY,
    Category.FAST_FOOD,
    Category.SUPERMARKET,
    Category.TELECOM,
    Category.BANK
]


@pytest.fixture
def add_max_count_categories(spends_client, remove_all_categories):
    [spends_client.add_category(category) for category in CATEGORIES]
