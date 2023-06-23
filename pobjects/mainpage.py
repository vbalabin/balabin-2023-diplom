from decimal import Decimal
from typing import List, Literal

from data.items import InventoryItem
from helpers.wrappers import wrapped_expect as expect
from pobjects.locators.mainlocators import MainLocators


class MainPage(MainLocators):
    def navigate(self):
        self.page.goto('/inventory.html')

    def get_all_inventory_items(self) -> List[InventoryItem]:
        result = list()
        self.inventory_item.wait_dom_loaded(500)
        for item in self.inventory_item.all():
            title = item.locator('//*[@class="inventory_item_name"]').inner_text()
            description = item.locator('//*[@class="inventory_item_desc"]').inner_text()
            price = Decimal(item.locator('//*[@class="inventory_item_price"]').inner_text()[1:])
            add_to_cart = item.locator('//*[text()="Add to cart"]')
            remove = item.locator('//*[text()="Remove"]')
            result.append(InventoryItem(title, description, price, add_to_cart, remove))
        return result

    def select_filter_option(self, option: Literal['az', 'za', 'lohi', 'hilo']):
        self.combobox_filter.select_option(option)

    def add_items_to_cart(self, count: int):
        for i, item in enumerate(self.get_all_inventory_items()):
            if i >= count:
                break
            item.add_to_cart.click()

    def assert_main_page_is_present(self):
        expect(self.page).to_have_url('/inventory.html')
