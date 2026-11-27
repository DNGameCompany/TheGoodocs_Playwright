from pages.base_page import BasePage
from playwright.sync_api import Page, Locator

from pages.locators.group_locators import GroupLocators


class GroupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._sort_filter_block = page.locator(GroupLocators.SORT_FILTER_BLOCK)
        self._templates_list_block = page.locator(GroupLocators.TEMPLATES_LIST_BLOCK)
        self._dropdown_meny_show = self._sort_filter_block.locator(GroupLocators.DROPDOWN_MENU_SHOW)

    def get_sort_dropdown(self) -> Locator:
        return self._sort_filter_block.get_by_role("button", name="Popularity")

    def get_sort_parameter_latest(self) -> Locator:
        return self._dropdown_meny_show.get_by_text("Latest")

    def click_sort_dropdown(self):
        self.get_sort_dropdown().click()

    def click_sort_parameter_latest(self):
        self.get_sort_parameter_latest().click()

    def get_first_template_card(self) -> Locator:
        return self._templates_list_block.locator(GroupLocators.FIRST_TEMPLATE_CARD).first

    def apply_sorting_by_latest(self):
        self.click_sort_dropdown()
        with self.get_current_page().expect_response(
                lambda r: "/ajax/category/load-more" in r.url and r.ok
        ):
            self.click_sort_parameter_latest()

    def templates_sorted(self, soft: bool = False):
        if soft:
            self.get_first_template_card().click(trial=True)
            return

    def add_get_parameters_in_url(self, parameters: str):
        current_url = self.get_current_url()
        if current_url:
            self.navigate_to(current_url + parameters)
