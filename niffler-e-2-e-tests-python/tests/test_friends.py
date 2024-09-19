from pages.main_page import main_page
from pages.friends_page import friends_page
import allure


@allure.story("Friends")
def test_empty_friends_table(login_app_user, logout):
        main_page.go_to_friends()
        friends_page.assert_empty_friends_table('There are no friends yet!')
