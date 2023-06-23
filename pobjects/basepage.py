from typing import TYPE_CHECKING

from playwright.sync_api import Page

from data.users import User
from pobjects.locators.commonlocators import CommonLocators

if TYPE_CHECKING:
    from pobjects.allpages import AllPages


class BasePage:
    base_url = '/'
    pobj: "AllPages" = None
    user: User = None

    def __init__(self, page: Page) -> None:
        self.page = page
        self.common = CommonLocators(page)
