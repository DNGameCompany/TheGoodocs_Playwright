from typing import Optional

from playwright.sync_api import Page, Response, Locator

from components.header import HeaderComponent
from pages.locators.components.header_locators import HeaderLocators


class BasePage:
    def __init__(self, page: Page):
        self.__page = page
        self.header = HeaderComponent(page.locator(HeaderLocators.HEADER_CONTAINER))

    def navigate_to(self, url: str) -> Optional[Response]:
        return self.__page.goto(url)

    def get_current_url(self) -> str:
        return self.__page.url

    def wait_for_url(self, expected_url: str, timeout: int = 5000):
        self.__page.wait_for_url(expected_url, timeout=timeout)

    def get_description(self) -> Locator:
        return self.__page.locator("meta[name='description']")

    def get_h1(self) -> Locator:
        return self.__page.get_by_role("heading", level=1)

    def get_current_page(self) -> Page:
        return self.__page

