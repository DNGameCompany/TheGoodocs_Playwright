from playwright.sync_api import Locator
from pages.locators.components.footer_locators import FooterLocators


class FooterComponent:
    def __init__(self, container: Locator):
        self.container = container

        self._lang_button = container.locator(FooterLocators.LANG_BUTTON)
        self._curr_lang = container.locator(FooterLocators.CURRENT_LANG)
        self._lang_list = container.locator(FooterLocators.LANG_LIST)

    def get_curr_lang(self) -> str:
        return self._curr_lang.inner_text()

    def change_lang(self, lang_name):
        self._lang_button.hover()
        self._lang_list.get_by_role("link", name=lang_name.capitalize, exact=True)

