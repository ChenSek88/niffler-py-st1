from http import HTTPStatus
import allure

from fixtures.client_fixtures import registration_client


@allure.tag("API")
@allure.epic("Registration")
class TestRegistration:
    def test_successful_registration(self, envs, user_for_reg, registration_client, user_db):
        username, password = user_for_reg
        registration_client.username = username
        with allure.step('Register user'):
            response = registration_client.register_user(username, password)
        with allure.step('Assert status code 201'):
            assert response.status_code == HTTPStatus.CREATED
        with allure.step('Assert username in db'):
            assert user_db.is_user_in_db(username)

    def test_bad_registration(self, envs, app_user, registration_client):
        username, password = app_user
        with allure.step('Register existing user'):
            response = registration_client.register_user(username, password)
            print(f"Статус код: {response}")
        with allure.step('Assert status code 400'):
            assert response.status_code == HTTPStatus.BAD_REQUEST
