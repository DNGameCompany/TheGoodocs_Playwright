import pytest
from playwright.async_api import expect

from pages.auth_page import AuthPage
from tests.conftest import UserCredentials
from utils.fake_user_data import fake
from utils.api_requests import authorization


@pytest.mark.auth
@pytest.mark.reset_password
class TestResetPassword:
    @pytest.mark.smoke
    def test_reset_password(self, log_in_page: AuthPage, mail_service, reset_password):
        reset_password_page = log_in_page.click_reset_password_link()

        mail_service.delete_all_emails()

        reset_password_page.request_reset_password_link(reset_password.email)

        reset_password_link = mail_service.reset_password_link(timeout_seconds=60)
        assert reset_password_link, "Посилання не прийшло поштою"

        reset_password_page.navigate_to(reset_password_link)

        new_password = fake.password()
        reset_password_page.set_new_password(new_password=new_password)

        user_new_password = UserCredentials(email=reset_password.email, password=new_password)

        assert authorization(user_new_password.email, user_new_password.password)["success"] is True


    @pytest.mark.smoke
    def test_reset_password_personal_acc(self, log_in_page: AuthPage, test_user):
        personal_account_page = log_in_page.login(test_user.email, test_user.password)
        new_password = fake.password()
        personal_account_page.reset_password(new_password)

        personal_account_page.reset_password_alert_is_visible()

        user_new_password = UserCredentials(email=test_user.email, password=new_password)

        assert authorization(user_new_password.email, user_new_password.password)["success"] is True



