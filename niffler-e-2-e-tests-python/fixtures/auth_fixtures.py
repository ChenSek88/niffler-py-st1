import pytest

from clients.oauth_client import OAuthClient
from models.config import Envs


@pytest.fixture(scope="session")
def auth_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password.get_secret_value())
