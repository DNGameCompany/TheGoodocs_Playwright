from pages.base_page import BasePage
from playwright.sync_api import Page, expect, Locator

from pages.reset_password_page import ResetPasswordPage
from pages.personal_account_page import PersonalAccountPage
from pages.locators.auth_locators import AuthLocators


class AuthPage(AuthLocators, BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Загальні елементи
        self._login_with_email_button = page.get_by_role("link", name="Continue with email")
        self._restore_password_link = page.get_by_text("Restore password").first

        # Контейнери форм для ізоляції локаторів
        self._login_form = page.locator(AuthLocators.LOGIN_FORM)
        self._registration_form = page.locator(AuthLocators.REGISTRATION_FORM)

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

    def click_reset_password_link(self) -> ResetPasswordPage:
        if self._restore_password_link.is_visible():
            self._restore_password_link.click()
            self.wait_for_url("**/personal/forgot-password/")
            return ResetPasswordPage(self.get_current_page())

    # --- Методи Авторизації ---
    def fill_login_email(self, email: str) -> None:
        self._login_email_field.fill(email)

    def fill_login_password(self, password: str) -> None:
        self._login_pass_field.fill(password)

    def click_log_in(self) -> None:
        self._log_in_button.click()

    def login(self, email: str, password: str, negative: bool = False) -> PersonalAccountPage:
        self.click_login_with_email_button()
        self.fill_login_email(email)
        self.fill_login_password(password)
        self.click_log_in()

        if not negative:
            return PersonalAccountPage(self.get_current_page())

    def user_logged_in_success(self):
        expected_url = "https://thegoodocs.com/personal/"
        self.wait_for_url(expected_url)

        assert self.get_current_url() == expected_url

    def email_field_is_required(self):
        expect(self._login_email_field).to_be_focused()
        validate_message = self._login_email_field.evaluate(self.VALIDATE_MESSAGE)

        assert validate_message == "Please fill in this field."


    def get_alert_error_text_login(self, error_text: str) -> Locator:
        return self._login_form.get_by_text(error_text)

    def login_error_alert_is_visible(self, error_text: str):
        expect(self.get_alert_error_text_login(error_text)).to_be_visible()

    # --- Методи Реєстрації ---
    def fill_reg_email(self, email: str) -> None:
        self._reg_email_field.fill(email)

    def fill_reg_password(self, password: str) -> None:
        self._reg_pass_field.fill(password)

    def click_sign_up(self) -> None:
        self._sign_up_button.click()

    def get_alert_error_text_register(self, error_text: str) -> Locator:
        return self._registration_form.get_by_text(error_text)

    def register_error_alert_is_visible(self, error_text: str):
        expect(self.get_alert_error_text_register(error_text)).to_be_visible()

    def registration(self, email: str, password: str) -> None:
        self.click_login_with_email_button()
        self.fill_reg_email(email)
        self.fill_reg_password(password)
        self.click_sign_up()