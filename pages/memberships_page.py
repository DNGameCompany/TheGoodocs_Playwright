import re

from pages.base_page import BasePage, Locator
from playwright.sync_api import Page, expect
from pages.locators.memberships_locators import MembershipsLocators


class MembershipsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._memberships_block = page.locator(MembershipsLocators.MEMBERSHIPS_BLOCK)
        self._memberships_checkout_modal = page.locator(MembershipsLocators.CHECKOUT_MODAL)
        self._password_field_checkout_modal = self._memberships_checkout_modal.get_by_placeholder("Password")
        self._fast_reg_form = self._memberships_checkout_modal.locator(MembershipsLocators.JS_FAST_REG)
        self._fast_login_form = self._memberships_checkout_modal.locator(MembershipsLocators.JS_FAST_LOGIN)

    def get_sub_button(self, plan: str, term: str) -> Locator:
        return self._memberships_block.locator(
            f'button.js-member-button[data-type="{plan}"][data-term="{term}"]'
        )

    def click_sub_button(self, plan: str, term: str):
        self.get_sub_button(plan=plan, term=term).click()

    def fill_email_field_checkout_modal_reg(self, email: str):
        self._fast_reg_form.get_by_role("textbox", name="E-mail address").fill(email.lower())

    def click_continue_to_secure_payment_button_checkout_modal(self):
        self._memberships_checkout_modal.get_by_role("button", name="Continue to Secure Payment").click()

    def enter_email_and_continue(self, email: str):
        self.fill_email_field_checkout_modal_reg(email=email)
        with self.get_current_page().expect_response(
                lambda r: "/ajax/quick-auth" in r.url and r.ok
        ):
            self.click_continue_to_secure_payment_button_checkout_modal()

        expect(self._password_field_checkout_modal).to_be_visible()

    def fill_password_field(self, password: str):
        self._fast_login_form.get_by_role("textbox", name="Password").fill(password)

    def click_submit_button(self):
        self._memberships_checkout_modal.get_by_role("button", name="Submit").click()

    def enter_password_and_submit(self, password: str):
        self.fill_password_field(password)
        self.click_submit_button()

    def wait_stripe_checkout(self):
        expect(self.get_current_page()).to_have_url(
            re.compile(r"^https://checkout\.stripe\.com/"), timeout=30_000
        )