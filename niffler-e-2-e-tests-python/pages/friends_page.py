import allure

from .base_page import BasePage


class FriendsPage(BasePage):

    def assert_empty_friends_table(self, expected_text):
        with allure.step(f'Assert that friends table is empty: {expected_text}'):
            self.assert_text('.people-content div', expected_text)


    def accept_invitation(self):
        with allure.step('Accept invitation'):
            self.find_element('[data-tooltip-id=submit-invitation] button').click()


    def decline_invitation(self):
        with allure.step('Decline invitation'):
            self.find_element('[data-tooltip-id=decline-invitation] button').click()


    def assert_message_in_table(self, expected_text):
        with allure.step(f'Assert message in table: {expected_text}'):
            self.assert_text('.abstract-table__buttons div', expected_text)


friends_page = FriendsPage()