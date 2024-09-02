from pages.main_page import main_page
from pages.people_page import people_page
from marks import Pages


@Pages.spending_page
def test_empty_people_table(logout):
        main_page.go_to_people()
        people_page.assert_empty_people_table('There are no other users yet!')


@Pages.spending_page
def test_user_exists_for_add_to_friends(registration, logout):
        friends_username, _ = registration
        main_page.go_to_people()
        people_page.assert_friend_in_table(friends_username)
        people_page.add_friend()
        main_page.assert_alert_message_and_close('Invitation is sent')
        #people_page.assert_pending_invitation()
