import allure

from clients.oauth_client import OAuthClient


@allure.epic("API")
@allure.story("Auth token")
def test_auth_token(app_user, envs):
    username, password = app_user
    return OAuthClient(envs).get_token(username, password)
