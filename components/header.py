from playwright.sync_api import Locator, expect
from pages.locators.components.header_locators import HeaderLocators


class HeaderComponent:
    def __init__(self, container: Locator):
        self.container = container

        self.search_field = container.get_by_placeholder("Search thousands of templates ...")
        self.search_button = container.get_by_role("button", name="search button")
        self.logo = container.locator(HeaderLocators.LOGO)
        self.templates_url = container.get_by_text("Templates")
        self.pricing_url = container.get_by_text("Pricing")

        #не залогінений
        self.log_in_button = container.locator(HeaderLocators.LOG_IN_BUTTON)
        self.sign_up_button = container.locator(HeaderLocators.SIGN_UP_BUTTON)

        #залогінений
        self.profile_avatar = container.locator(HeaderLocators.PROFILE_AVATAR)


    def search_for_button(self, query: str):
        self.search_field.fill(query)
        self.search_button.click()

    def search_for_enter(self, query: str):
        self.search_field.fill(query)
        self.search_field.press("Enter")

    def click_login(self):
        self.log_in_button.click()

    def click_sign_up(self):
        self.sign_up_button.click()

    def is_unauthorized(self):
        return expect(self.log_in_button).to_be_visible()

    def verify_is_logged_in(self):
        return expect(self.profile_avatar).to_be_visible()