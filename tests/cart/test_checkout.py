import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from pobjects.allpages import AllPages
from helpers.wrappers import wrapped_expect as expect


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.CART)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Корзина. "Checkout"')
def test_remove_from_cart(page: Page, pobj: AllPages):
    items_number = 3
    with allure.step('Предусловие: Авторизация, добавлены товары в корзину, открыта корзина'):
        pobj.login.do_login()
        pobj.main.add_items_to_cart(items_number)
        pobj.main.button_cart.click()
        pobj.cart.cart_item.wait_dom_loaded(timeout=500)
    with allure.step('1 клик "Checkout"'):
        pobj.cart.button_checkout.click()
    with allure.step('2 клик "Cancel"'):
        pobj.checkout.button_cancel.click()
    with allure.step('3 клик "Checkout"'):
        pobj.cart.button_checkout.click()
    with allure.step('4 Заполнить поля Имени, индекса, клик "Checkout"'):
        pobj.checkout.input_first_name.fill('Test')
        pobj.checkout.input_second_name.fill('Test')
        pobj.checkout.input_zip_code.fill('001001')
    with allure.step('5 клик "Continue"'):
        pobj.checkout.button_continue.click()
    with allure.step('6 клик "Finish"'):
        pobj.checkout.button_finish.click()
    with allure.step('6 клик "Back Home"'):
        pobj.checkout.button_back_home.click()
    with allure.step('Проверка: открыта Главная'):
        expect(page).to_have_url('/inventory.html')
