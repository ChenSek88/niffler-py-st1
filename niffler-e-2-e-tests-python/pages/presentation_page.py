from .base_page import BasePage
import allure


class PresentationPage(BasePage):

    def assert_header_title(self, expected_text):
        with allure.step('Assert presentation header title'):
            self.assert_text('.main__header', expected_text)

    def go_to_login(self):
        with allure.step('Go to login page'):
            self.find_element('a[href*=redirect]').click()

    def go_to_register(self):
        with allure.step('Go to register page'):
            self.find_element('a[href*=redirect]').click()


presentation_page = PresentationPage()