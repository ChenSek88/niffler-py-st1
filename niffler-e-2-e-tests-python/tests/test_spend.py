from pages.main_page import main_page
from pages.profile_page import profile_page


AMOUNT = '50000'
CATEGORY = 'SCHOOL'
DESCRIPTION = 'QA_GURU PYTHON ADVANCED'


def test_add_spending(login_app_user, logout):
        main_page.go_to_profile()
        profile_page.add_category(CATEGORY)
        main_page.assert_alert_message_and_close('New category added')
        main_page.go_to_main_page()
        main_page.add_spending(CATEGORY, AMOUNT, DESCRIPTION)
        main_page.assert_alert_message_and_close('Spending successfully added')
        main_page.spending_added(AMOUNT, CATEGORY, DESCRIPTION)
