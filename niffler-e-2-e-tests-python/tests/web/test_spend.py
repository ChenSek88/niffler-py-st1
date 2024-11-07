import allure

from pages.main_page import main_page
from marks import TestData
from models.enums import Category, Spend


@allure.tag("WEB")
@allure.epic("Spending")
class TestSpendPage:
    def test_spending_title_exists(self, login_app_user):
        main_page.assert_spending_section_title('History of spendings')

    def test_add_spending_without_category(self, login_app_user):
        main_page.add_new_spending()
        main_page.assert_spending_form_error('Category is required')

    @TestData.category(Category.SCHOOL)
    def test_add_spending(self, category, login_app_user, remove_all_spends):
        main_page.fill_spending_fields(Category.SCHOOL, Spend.AMOUNT, Spend.DESCRIPTION)
        main_page.add_new_spending()
        main_page.assert_alert_message('Spending successfully added')
        main_page.spending_added(Spend.AMOUNT, Category.SCHOOL, Spend.DESCRIPTION)

    @TestData.category(Category.SCHOOL)
    @TestData.spends(Spend.TEST_DATA)
    def test_delete_spending(self, category, spends, login_app_user):
        main_page.spending_added(Spend.AMOUNT, Category.SCHOOL, Spend.DESCRIPTION)
        main_page.delete_spending()
        main_page.assert_alert_message('Spendings deleted')
        main_page.spending_table_is_empty('No spendings provided yet!')
