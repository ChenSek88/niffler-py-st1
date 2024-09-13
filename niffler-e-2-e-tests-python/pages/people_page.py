import allure

from .base_page import BasePage
from selene import have


class PeoplePage(BasePage):

    def assert_empty_people_table(self, expected_text):
        with allure.step('Assert empty people table'):
            self.assert_text('.people-content div', expected_text)


    def assert_people_in_table(self, username):
        with allure.step(f'Assert user: {username} exists in table'):
            people_table = self.find_element('.people-content tbody tr')
            elements = people_table.all('td')
            elements.should(have._texts_like(username))


    def add_friend(self):
        with allure.step('Add friend'):
            self.find_element('[data-tooltip-id=add-friend] button').click()


    def assert_message_in_table(self, expected_text):
        with allure.step(f'Assert message in table: {expected_text}'):
            self.assert_text('.abstract-table__buttons div', expected_text)


    def accept_invitation(self):
        with allure.step('Accept invitation'):
            self.find_element('[data-tooltip-id=submit-invitation] button').click()


    def decline_invitation(self):
        with allure.step('Decline invitation'):
            self.find_element('[data-tooltip-id=decline-invitation] button').click()


    def add_friend_button_exists(self):
        with allure.step('Assert that invitation declined'):
            self.find_element('[data-tooltip-id=add-friend] button')


people_page = PeoplePage()