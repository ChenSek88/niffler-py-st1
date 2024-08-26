from pages.main_page import main_page
from pages.people_page import people_page
from marks import Pages


@Pages.spending_page
def test_empty_friends_table(logout):
        main_page.go_to_people()
        people_page.assert_empty_people_table('There are no other users yet!')
