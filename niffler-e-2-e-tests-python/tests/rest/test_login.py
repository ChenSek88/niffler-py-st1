from clients.oauth_client import OAuthClient


def test_get_token(app_user, envs):
    username, password = app_user
    return OAuthClient(envs).get_token(username, password)
