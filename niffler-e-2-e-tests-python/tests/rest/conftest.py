import pytest
from conftest import envs


@pytest.fixture(scope="session")
def app_user(envs):
    return envs.test_username, envs.test_password.get_secret_value()