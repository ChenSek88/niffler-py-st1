from .base_page import BasePage
from selene import have


class MainPage(BasePage):

    def logout(self):
        self.find_element('.header__logout button').click()


    def assert_alert_message_and_close(self, expected_text):
        self.assert_text('.Toastify__toast-icon ~ div', expected_text)
        self.find_element('.Toastify__close-button svg').click()


    def assert_main_page_title(self, expected_text):
        self.assert_text('.header__title', expected_text)


    def go_to_profile(self):
        self.find_element('a[href*=profile]').click()


    def go_to_main_page(self):
        self.find_element('a[href*=main]').click()


    def add_spending(self, CATEGORY, AMOUNT, DESCRIPTION):
        self.find_element('.add-spending__form .select-wrapper input').click()
        self.find_element('.add-spending__form .select-wrapper input').set_value(CATEGORY)
        self.find_element("div[id*='react-select']").should(have.text(CATEGORY)).click()
        self.find_element('.add-spending__form [name=amount]').set_value(AMOUNT)
        self.find_element('.add-spending__form [name=description]').set_value(DESCRIPTION)
        self.find_element('.add-spending__form .button').click()


    def spending_added(self, AMOUNT, CATEGORY, DESCRIPTION):
        spending_table = self.find_element('.spendings-table tbody tr')
        elements = spending_table.all('td .value-container')
        elements.should(have._texts_like(AMOUNT, CATEGORY, DESCRIPTION))


main_page=MainPage()