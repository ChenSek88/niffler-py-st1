from pages.main_page import main_page
from pages.friends_page import friends_page
from marks import Pages


@Pages.spending_page
def test_empty_friends_table(logout):
        main_page.go_to_friends()
        friends_page.assert_empty_friends_table('There are no friends yet!')
