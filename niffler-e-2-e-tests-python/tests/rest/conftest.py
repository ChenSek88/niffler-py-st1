import pytest
from conftest import envs

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.database_fixtures",
                  "fixtures.generate_data_fixtures"]


@pytest.fixture(scope="session")
def app_user(envs):
    return envs.test_username, envs.test_password.get_secret_value()
