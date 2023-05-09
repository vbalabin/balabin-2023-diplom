from playwright.sync_api import Page
# from pobjects.allpages import AllPages
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pobjects.allpages import AllPages


class Base:
    base_url = '/'
    pobj: "AllPages" = None

    def __init__(self, page: Page) -> None:
        self.page = page
