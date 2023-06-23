from playwright.sync_api import Page

from pobjects.basepage import BasePage

from helpers.wrappers import LocatorDescriptor


class LoginLocators(BasePage):
    input_username = LocatorDescriptor()
    'поле ввода username'

    input_password = LocatorDescriptor()
    'поле ввода password'

    button_login = LocatorDescriptor()
    'кнопка "Login"'

    label_locked_out = LocatorDescriptor()
    'сообщение "Epic sadface: Sorry, this user has been locked out."'

    def __init__(self, page: Page):
        super().__init__(page)
        self.input_username = page.locator('//input[@id="user-name"]')
        self.input_password = page.locator('//input[@id="password"]')
        self.button_login = page.locator('//input[@id="login-button"]')
        self.label_locked_out = page.locator('//*[@data-test="error"][contains(text(), "locked out")]')
