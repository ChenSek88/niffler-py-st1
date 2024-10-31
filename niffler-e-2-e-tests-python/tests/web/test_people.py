from pages.main_page import main_page
from pages.people_page import people_page
from pages.login_page import login_page
import allure


@allure.epic("WEB")
@allure.story("People")
def test_empty_people_table(login_app_user):
    main_page.go_to_people()
    people_page.assert_empty_people_table('There are no other users yet!')


@allure.epic("WEB")
@allure.story("People")
def test_user_exists_for_add_to_friends(registration, login_app_user):
    username, _ = registration
    main_page.go_to_people()
    people_page.assert_people_in_table(username)


@allure.epic("WEB")
@allure.story("People")
def test_add_friend(registration, login_app_user):
    username, _ = registration
    main_page.go_to_people()
    people_page.assert_people_in_table(username)
    people_page.add_friend()
    main_page.assert_alert_message('Invitation is sent')
    people_page.assert_message_in_table('Pending invitation')


@allure.epic("WEB")
@allure.story("People")
def test_accept_friend_invitation(registration, friend_request):
    username, password = registration
    friend_request(username)
    login_page.login(username, password)
    main_page.go_to_people()
    people_page.accept_invitation()
    main_page.assert_alert_message('Invitation is accepted')
    people_page.assert_message_in_table('You are friends')


@allure.epic("WEB")
@allure.story("People")
def test_decline_friend_invitation(registration, friend_request):
    username, password = registration
    friend_request(username)
    login_page.login(username, password)
    main_page.go_to_people()
    people_page.decline_invitation()
    main_page.assert_alert_message('Invitation is declined')
    people_page.add_friend_button_exists()
