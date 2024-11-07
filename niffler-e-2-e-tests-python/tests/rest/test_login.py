import allure

from clients.oauth_client import OAuthClient


@allure.tag("API")
@allure.epic("Auth token")
def test_auth_token(app_user, envs):
    username, password = app_user
    oauth_client = OAuthClient(envs)
    token = oauth_client.get_token(username, password)
    with allure.step(f'Token is not none'):
        assert token is not None
