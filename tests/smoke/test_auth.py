import pytest

from pages.auth_page import AuthPage
from test_data.subscriptions_data import SubPlans, SubTerms


@pytest.mark.auth
class TestAuth:
    @pytest.mark.serial
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.positive
    def test_authorisation_with_email(self, test_user, log_in_page):
        log_in_page.login(test_user.email, test_user.password)
        log_in_page.user_logged_in_success()

    @pytest.mark.serial
    @pytest.mark.smoke
    @pytest.mark.register
    @pytest.mark.positive
    def test_registration_with_email(self, sign_up_page, registration_user_real_data, mail_service):
        mail_service.delete_all_emails()

        sign_up_page.registration(registration_user_real_data.email, registration_user_real_data.password)

        activation_url = mail_service.verification_link(timeout_seconds=30)

        assert activation_url != "", "Посилання не прийшло поштою"

        sign_up_page.navigate_to(activation_url)
        sign_up_page.header.verify_is_logged_in()

    @pytest.mark.serial
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.positive
    @pytest.mark.memverships
    def test_login_with_email_memberships(self, memberships_page, test_user):
        memberships_page.click_sub_button(SubPlans.INDIVIDUAL, SubTerms.MONTHLY)
        memberships_page.enter_email_and_continue(test_user.email)
        memberships_page.enter_password_and_submit(test_user.password)
        memberships_page.wait_stripe_checkout()

        memberships_page.navigate_to("https://thegoodocs.com/personal/")
        AuthPage(memberships_page.get_current_page()).user_logged_in_success()



