from playwright.sync_api import Page

from pobjects.basepage import BasePage

from helpers.wrappers import LocatorDescriptor


class MainLocators(BasePage):
    button_cart = LocatorDescriptor()
    'кнопка корзины сверху-справа'

    combobox_filter = LocatorDescriptor()
    'комбобокс фильтров'

    inventory_item = LocatorDescriptor()
    'любой товар на главной'

    def __init__(self, page: Page):
        super().__init__(page)
        self.button_cart = page.locator('//a[@class="shopping_cart_link"]')
        self.combobox_filter = page.locator("//select[@data-test='product_sort_container']")
        self.inventory_item = page.locator("//div[@class='inventory_item']")
