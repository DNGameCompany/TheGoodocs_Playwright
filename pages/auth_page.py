from pages.base_page import BasePage
from playwright.sync_api import Page


class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Загальні елементи
        self._login_with_email_button = page.get_by_role("link", name="Continue with email")

        # Контейнери форм для ізоляції локаторів
        self._login_form = page.locator("#form-login")
        self._registration_form = page.locator("#form-registration")

        # Локатори форми Авторизації (Login)
        self._login_email_field = self._login_form.locator("input[name='email']")
        self._login_pass_field = self._login_form.locator("input[name='password']")
        self._log_in_button = self._login_form.get_by_role("button", name="LOG IN")

        # Локатори форми Реєстрації (Registration)
        self._reg_email_field = self._registration_form.locator("input[name='re-name']")
        self._reg_pass_field = self._registration_form.locator("input[name='re-password']")
        self._sign_up_button = self._registration_form.get_by_role("button", name="SIGN UP")

    def click_login_with_email_button(self) -> None:
        if self._login_with_email_button.is_visible():
            self._login_with_email_button.click()

    # --- Методи Авторизації ---
    def fill_login_email(self, email: str) -> None:
        self._login_email_field.fill(email)

    def fill_login_password(self, password: str) -> None:
        self._login_pass_field.fill(password)

    def click_log_in(self) -> None:
        self._log_in_button.click()

    def login(self, email: str, password: str) -> None:
        self.click_login_with_email_button()
        self.fill_login_email(email)
        self.fill_login_password(password)
        self.click_log_in()

    # --- Методи Реєстрації ---
    def fill_reg_email(self, email: str) -> None:
        self._reg_email_field.fill(email)

    def fill_reg_password(self, password: str) -> None:
        self._reg_pass_field.fill(password)

    def click_sign_up(self) -> None:
        self._sign_up_button.click()

    def registration(self, email: str, password: str) -> None:
        self.click_login_with_email_button()
        self.fill_reg_email(email)
        self.fill_reg_password(password)
        self.click_sign_up()