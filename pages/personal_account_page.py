from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect


class PersonalAccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self._new_password_field = page.get_by_placeholder("New Password")
        self._reset_password_button = page.get_by_role("button", name="Reset password")
        self._reset_password_alert_success = page.get_by_text("Change password successfully")

    def get_new_password_field(self) -> Locator:
        return self._new_password_field

    def get_reset_password_button(self) -> Locator:
        return self._reset_password_button

    def get_reset_password_alert_success(self) -> Locator:
        return self._reset_password_alert_success

    def get_reset_password_alert_success_text(self) -> str:
        return self.get_reset_password_alert_success().text_content()

    def fill_new_password_field(self, new_password: str):
        self.get_new_password_field().fill(new_password)

    def click_reset_password_button(self):
        self.get_reset_password_button().click()

    def reset_password(self, new_password: str):
        self.fill_new_password_field(new_password)
        self.click_reset_password_button()

    def reset_password_alert_is_visible(self):
        expect(self.get_reset_password_alert_success()).to_be_visible()


