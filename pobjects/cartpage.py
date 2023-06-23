from decimal import Decimal
from typing import List

from data.items import InventoryItem
from helpers.wrappers import WrappedLocator
from pobjects.locators.cartlocators import CartLocators


class CartPage(CartLocators):
    def navigate(self):
        self.page.goto('/cart.html')

    def process_cart_item(self, cart_item: WrappedLocator):
        title = cart_item.locator("//a[@id]").inner_text()
        description = cart_item.locator("//div[@class='inventory_item_desc']").inner_text()
        price = Decimal(cart_item.locator("//*[@class='inventory_item_price']").inner_text()[1:])
        remove = cart_item.locator("//button[text()='Remove']")
        return (title, description, price, remove)

    def get_all_inventory_items(self) -> List[InventoryItem]:
        result = list()
        self.cart_item.wait_dom_loaded(500)
        for item in self.cart_item.all():
            title, description, price, remove = self.process_cart_item(item)
            result.append(InventoryItem(title, description, price, None, remove))
        return result

    def clear_cart(self, items: List[InventoryItem] = None):
        if items is None:
            items = self.get_all_inventory_items()

        for _ in items:
            remove = self.process_cart_item(self.cart_item.first)[-1]
            remove.click()
            remove.wait_dom_loaded(250)
