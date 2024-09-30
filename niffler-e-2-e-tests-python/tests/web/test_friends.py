from pages.login_page import login_page
from pages.main_page import main_page
from pages.friends_page import friends_page
import allure


@allure.story("Friends")
def test_empty_friends_table(login_app_user, logout):
    main_page.go_to_friends()
    friends_page.assert_empty_friends_table('There are no friends yet!')


@allure.story("Friends")
def test_accept_friend_invitation(registration, friend_request, logout):
    username, password = registration
    friend_request(username)
    login_page.login(username, password)
    main_page.go_to_friends()
    friends_page.accept_invitation()
    main_page.assert_alert_message_and_close('Invitation is accepted')
    friends_page.assert_message_in_table('You are friends')


@allure.story("Friends")
def test_decline_friend_invitation(registration, friend_request, logout):
    username, password = registration
    friend_request(username)
    login_page.login(username, password)
    main_page.go_to_friends()
    friends_page.decline_invitation()
    main_page.assert_alert_message_and_close('Invitation is declined')
    friends_page.assert_empty_friends_table('There are no friends yet!')