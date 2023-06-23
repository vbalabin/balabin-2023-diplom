import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from data.users import locked_out_user
from helpers.wrappers import wrapped_expect as expect
from pobjects.allpages import AllPages


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.AUTOREG)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title(f'Авторизация {locked_out_user.login}')
def test_authorization_lou(page: Page, pobj: AllPages):
    with allure.step('Предусловие: Перейти на страницу авторизации'):
        pobj.login.navigate()
    with allure.step('1 Заполнить поле "Логин"'):
        pobj.login.input_username.fill(locked_out_user.login)
    with allure.step('2 Заполнить поле "Пароль"'):
        pobj.login.input_password.fill(locked_out_user.password)
    with allure.step('3 Клик на кнопку "Login"'):
        pobj.login.button_login.click()
    with allure.step('проверка: показывается сообщение о блокировке'):
        expect(pobj.login.label_locked_out).to_be_visible()
