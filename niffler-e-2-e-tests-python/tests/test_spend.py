import allure

from pages.main_page import main_page
from marks import Pages, TestData
from models.spend import SpendAdd


AMOUNT = 50000
CATEGORY = "SCHOOL"
DESCRIPTION = "QA-GURU PYTHON ADVANCED"


@allure.story("Spending")
def test_spending_title_exists(login_app_user, logout):
        main_page.assert_spending_section_title('History of spendings')


@TestData.category(CATEGORY)
@allure.story("Spending")
def test_add_spending(category, login_app_user, remove_all_spends, logout):
        main_page.add_spending(CATEGORY, AMOUNT, DESCRIPTION)
        main_page.assert_alert_message_and_close('Spending successfully added')
        main_page.spending_added(AMOUNT, CATEGORY, DESCRIPTION)


@TestData.category(CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=AMOUNT,
        description=DESCRIPTION,
        category=CATEGORY,
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB"
    )
)
@allure.story("Spending")
def test_delete_spending(category, spends, login_app_user, logout):
        main_page.spending_added(AMOUNT, CATEGORY, DESCRIPTION)
        main_page.delete_spending()
        main_page.assert_alert_message_and_close('Spendings deleted')
        main_page.spending_table_is_empty('No spendings provided yet!')
