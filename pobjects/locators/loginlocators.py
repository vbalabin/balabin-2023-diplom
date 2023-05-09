from playwright.sync_api import Page

from pobjects.base import Base

from helpers.wrappers import LocatorDescriptor


class LoginLocators(Base):
    input_username = LocatorDescriptor()
    'asdasd'
    input_password = LocatorDescriptor()
    'asdasd'
    button_login = LocatorDescriptor()
    'asdasd'

    def __init__(self, page: Page):
        super().__init__(page)
        self.input_username = page.locator('//input[@id="user-name"]')
        self.input_password = page.locator('//input[@id="password"]')
        self.button_login = page.locator('//input[@id="login-button"]')
