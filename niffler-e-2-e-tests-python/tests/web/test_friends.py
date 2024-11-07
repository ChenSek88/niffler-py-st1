from pages.login_page import login_page
from pages.main_page import main_page
from pages.friends_page import friends_page
import allure


@allure.tag("WEB")
@allure.epic("Friends page")
class TestFriendsPage:
    def test_empty_friends_table(self, login_app_user):
        main_page.go_to_friends()
        friends_page.assert_empty_friends_table('There are no friends yet!')

    def test_accept_friend_invitation(self, registration, friend_request):
        username, password = registration
        friend_request(username)
        login_page.login(username, password)
        main_page.go_to_friends()
        friends_page.accept_invitation()
        main_page.assert_alert_message('Invitation is accepted')
        friends_page.assert_message_in_table('You are friends')

    def test_decline_friend_invitation(self, registration, friend_request):
        username, password = registration
        friend_request(username)
        login_page.login(username, password)
        main_page.go_to_friends()
        friends_page.decline_invitation()
        main_page.assert_alert_message('Invitation is declined')
        friends_page.assert_empty_friends_table('There are no friends yet!')