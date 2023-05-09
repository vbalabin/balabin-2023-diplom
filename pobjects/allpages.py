from typing import Any
from playwright.sync_api import Page
from .loginpage import LoginPage
from .mainpage import MainPage


class AllPages:
    def __init__(self) -> None:
        self.__page: Page = None
        self.login: LoginPage = None
        self.main: MainPage = None

    def __getattribute__(self, __name: str) -> Any:
        if __name == '_lazy_init' or object.__getattribute__(self, '_AllPages__page'):
            return object.__getattribute__(self, __name)
        else:
            raise ValueError('self.__page is None, initialization has not been finished!!')

    def _lazy_init(self, page: Page) -> None:
        self.__page = page
        self.login = LoginPage(page)
        self.main = MainPage(page)


PAGES = AllPages()
