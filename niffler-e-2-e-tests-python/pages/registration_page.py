from .base_page import BasePage
import allure


class RegistrationPage(BasePage):

    def user_registration(self, username, password):
        with allure.step(f'Registration with username: {username}'):
            self.open_url('http://frontend.niffler.dc')
            self.find_element('a[href*=register]').click()
            self.find_element('#username').set_value(username)
            self.find_element('#password').set_value(password)
            self.find_element('#passwordSubmit').set_value(password)
            self.find_element('[type="submit"]').click()

    def registration_with_diff_passwords(self, username, password):
        with allure.step(f'Registration with username: {username} with different passwords'):
            self.open_url('http://frontend.niffler.dc')
            self.find_element('a[href*=register]').click()
            self.find_element('#username').set_value(username)
            self.find_element('#password').set_value(password)
            self.find_element('#passwordSubmit').set_value('bad' + password)
            self.find_element('[type="submit"]').click()

    def assert_bad_registration(self, expected_text):
        with allure.step(f'Assert bad registration: {expected_text}'):
            self.assert_text('#register-form .form__error', expected_text)


registration_page=RegistrationPage()