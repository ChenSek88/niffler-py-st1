from http import HTTPStatus

import allure
import requests


@allure.epic("API")
@allure.story("Registration")
def test_successful_registration(envs, user_for_reg, user_in_db):
    cookie = requests.get(f"{envs.frontend_url}:9000/register").headers['x-xsrf-token']
    username, password = user_for_reg
    user_data = {"_csrf": cookie, "username": username, "password": password, "passwordSubmit": password}
    with allure.step('Send post request on /register'):
        response = requests.post(f"{envs.frontend_url}:9000/register",
            data=user_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'XSRF-TOKEN={cookie}'}
        )
    with allure.step('Assert status code 201'):
        assert response.status_code == HTTPStatus.CREATED
    with allure.step('Assert username in db'):
        assert user_in_db(username) == username


@allure.epic("API")
@allure.story("Registration")
def test_bad_registration(envs, app_user, user_in_db):
    cookie = requests.get(f"{envs.frontend_url}:9000/register").headers['x-xsrf-token']
    username, password = app_user
    user_data = {"_csrf": cookie, "username": username, "password": password, "passwordSubmit": password}
    with allure.step('Send post request on /register'):
        response = requests.post(f"{envs.frontend_url}:9000/register",
            data=user_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'XSRF-TOKEN={cookie}'}
        )
    with allure.step('Assert status code 400'):
        assert response.status_code == HTTPStatus.BAD_REQUEST
