from .base_page import BasePage


class LoginPage(BasePage):

    def login(self, username, password):
        self.open_url('http://frontend.niffler.dc')
        self.find_element('a[href*=redirect]').click()
        self.find_element('[name=username]').set_value(username)
        self.find_element('[name=password]').set_value(password)
        self.find_element('[type=submit]').click()


    def assert_bad_login(self, expected_text):
        self.assert_text('[action*=login] .form__error', expected_text)


login_page = LoginPage()