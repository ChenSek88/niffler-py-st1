from pages.main_page import main_page
from pages.profile_page import profile_page
from marks import Pages, TestData
from time import sleep


AMOUNT = "50000"
CATEGORY = "SCHOOL"
DESCRIPTION = "QA-GURU PYTHON ADVANCED"


@Pages.spending_page
def test_spending_title_exists(logout):
        main_page.assert_spending_section_title('History of spendings')


@Pages.spending_page
def test_add_spending(remove_all_spends, logout):
        main_page.go_to_profile()
        profile_page.add_category(CATEGORY)
        main_page.assert_alert_message_and_close('New category added')
        main_page.go_to_main_page()
        main_page.add_spending(CATEGORY, AMOUNT, DESCRIPTION)
        main_page.assert_alert_message_and_close('Spending successfully added')
        main_page.spending_added(AMOUNT, CATEGORY, DESCRIPTION)


@Pages.spending_page
@TestData.category(CATEGORY)
@TestData.spends({
        "amount": AMOUNT,
        "description": DESCRIPTION,
        "category": CATEGORY,
        "spendDate": "2024-08-25T18:39:27.955Z",
        "currency": "RUB"
    })
def test_delete_spending(category, spends, logout):
        main_page.spending_added(AMOUNT, CATEGORY, DESCRIPTION)
        main_page.delete_spending()
        main_page.assert_alert_message_and_close('Spendings deleted')
        main_page.spending_table_is_empty('No spendings provided yet!')
