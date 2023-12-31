import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from data.users import standard_user
from helpers.wrappers import wrapped_expect as expect
from pobjects.allpages import AllPages


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.AUTOREG)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title(f'Авторизация {standard_user.login}')
def test_authorization_su(page: Page, pobj: AllPages):
    with allure.step('Предусловие: Перейти на страницу авторизации'):
        pobj.login.navigate()
    with allure.step('1 Заполнить поле "Логин"'):
        pobj.login.input_username.fill(standard_user.login)
    with allure.step('2 Заполнить поле "Пароль"'):
        pobj.login.input_password.fill(standard_user.password)
    with allure.step('3 Клик на кнопку "Login"'):
        pobj.login.button_login.click()
    with allure.step('Проверка: открыта Главная'):
        expect(page).to_have_url('/inventory.html')
