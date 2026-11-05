from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self._email_field = page.get_by_placeholder("Enter your email")
        self._send_button = page.get_by_role("button", name="SEND")
        self._new_password_field = page.get_by_placeholder("New password")


    def get_email_field(self) -> Locator:
        return self._email_field

    def get_send_button(self) -> Locator:
        return self._send_button

    def get_new_password_field(self) -> Locator:
        return self._new_password_field


    def fill_email_field(self, email:str):
        self.get_email_field().fill(email)

    def fill_new_password_field(self, new_password:str):
        self.get_new_password_field().fill(new_password)

    def click_send_button(self):
        self.get_send_button().click()



    def request_reset_password_link(self, email:str):
        self.fill_email_field(email=email)
        self.click_send_button()

    def set_new_password(self, new_password:str):
        self.fill_new_password_field(new_password)
        self.click_send_button()
