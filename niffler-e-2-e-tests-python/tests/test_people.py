from pages.main_page import main_page
from pages.people_page import people_page
from marks import Pages
from pages.login_page import login_page


@Pages.spending_page
def test_empty_people_table(logout):
        main_page.go_to_people()
        people_page.assert_empty_people_table('There are no other users yet!')


@Pages.spending_page
def test_user_exists_for_add_to_friends(registration, logout):
        username, _ = registration
        main_page.go_to_people()
        people_page.assert_people_in_table(username)


@Pages.spending_page
def test_add_friend(registration, logout):
        username, _ = registration
        main_page.go_to_people()
        people_page.assert_people_in_table(username)
        people_page.add_friend()
        main_page.assert_alert_message_and_close('Invitation is sent')
        people_page.assert_message_in_table('Pending invitation')


@Pages.spending_page
def test_accept_friend_invitation(registration, friend_request, logout):
        username, password = registration
        friend_request(username)
        main_page.logout()
        login_page.login(username, password)
        main_page.go_to_people()
        people_page.accept_invitation()
        main_page.assert_alert_message_and_close('Invitation is accepted')
        people_page.assert_message_in_table('You are friends')


@Pages.spending_page
def test_decline_friend_invitation(registration, friend_request, logout):
        username, password = registration
        friend_request(username)
        main_page.logout()
        login_page.login(username, password)
        main_page.go_to_people()
        people_page.decline_invitation()
        main_page.assert_alert_message_and_close('Invitation is declined')
        people_page.add_friend_button_exists()
