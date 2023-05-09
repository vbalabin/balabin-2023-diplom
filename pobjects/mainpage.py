import allure
from pobjects.locators.mainlocators import MainLocators
from helpers.wrappers import wrapped_expect as expect


class MainPage(MainLocators):
    def navigate(self):
        self.page.goto('/inventory.html')

    @allure.step('проверка: мы на Главной')
    def assert_main_page_is_present(self):
        expect(self.page).to_have_url('/inventory.html')
