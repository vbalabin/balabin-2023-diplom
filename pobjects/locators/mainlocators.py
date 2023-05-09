from playwright.sync_api import Page

from pobjects.base import Base

from helpers.wrappers import LocatorDescriptor


class MainLocators(Base):
    button_cart = LocatorDescriptor()
    'кнопка корзины сверху-справа'

    def __init__(self, page: Page):
        super().__init__(page)
        self.button_cart = page.locator('//a[@class="shopping_cart_link"]')
