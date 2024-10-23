from .base_page import BasePage
import allure


class LoginPage(BasePage):

    def login(self, username, password):
        with allure.step(f'Login with username: {username}'):
            self.open_url('http://frontend.niffler.dc')
            self.find_element('a[href*=redirect]').click()
            self.find_element('[name=username]').set_value(username)
            self.find_element('[name=password]').set_value(password)
            self.find_element('[type=submit]').click()

    def assert_bad_login(self, expected_text):
        with allure.step(f'Assert bad login: {expected_text}'):
            self.assert_text('[action*=login] .form__error', expected_text)


login_page = LoginPage()