import allure

from .base_page import BasePage


class FriendsPage(BasePage):

    def assert_empty_friends_table(self, expected_text):
        with allure.step(f'Assert that friends table is empty: {expected_text}'):
            self.assert_text('.people-content div', expected_text)


    def accept_invitation(self):
        self.find_element('[data-tooltip-id=submit-invitation] button').click()


    def decline_invitation(self):
        self.find_element('[data-tooltip-id=decline-invitation] button').click()


friends_page = FriendsPage()