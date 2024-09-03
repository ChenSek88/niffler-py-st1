from pages.registration_page import registration_page
from pages.login_page import login_page
from pages.main_page import main_page
from time import sleep


def test_registration_successful(user_for_reg, delete_user, logout):
        username, password = user_for_reg
        registration_page.user_registration(username, password)
        login_page.login(username, password)
        main_page.assert_main_page_title('Niffler. The coin keeper.')
        delete_user(username)


def test_registration_with_diff_passwords(user_for_reg):
        username, password = user_for_reg
        registration_page.registration_with_diff_passwords(username, password)
        registration_page.assert_bad_registration('Passwords should be equal')


def test_registration_an_existing_user(registration):
        username, password = registration
        registration_page.user_registration(username, password)
        registration_page.assert_bad_registration(f'Username `{username}` already exists')
        sleep(5)
        # Форма регистрации восстанавливает запись в таблице user (niffler-userdata) после некоторой задержки.
        # Это происходит даже в случае если срабатывает исключение 'Username `{username}` already exists'
        # Если удалить запись с этим пользователем сразу, то она через некоторое время появится снова
        # Видимо в момент удаления записи, запрос клиента встает в очередь, хоть сервер и возвращает ошибку, возможно баг
