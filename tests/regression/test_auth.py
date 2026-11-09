from pickle import FALSE

import pytest
from utils.fake_user_data import fake, fake_ua
from test_data.emails import EMPTY_EMAIL_CASES, INVALID_EMAIL_CASES


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.login
class TestAuth:
    @pytest.mark.negative
    @pytest.mark.parametrize("empty_email", EMPTY_EMAIL_CASES)
    def test_login_required_field_email(self, log_in_page, test_user_data, empty_email):
        log_in_page.login(email=empty_email, password=test_user_data.password, negative=True)
        match empty_email:
            case "":
                log_in_page.email_field_is_required()
            case _ if empty_email.isspace():
                log_in_page.login_error_alert_is_visible("The email field is required.")


    @pytest.mark.negative
    def test_login_required_field_password(self, log_in_page, test_user_data):
        log_in_page.login(email=test_user_data.email, password="")
        log_in_page.email_field_is_required()

    @pytest.mark.negative
    @pytest.mark.parametrize("test_email", INVALID_EMAIL_CASES)
    def test_login_validate_field_email(self, log_in_page, test_email, cleanup_registered_user):
        log_in_page.login(email=test_email, password=fake.password(), negative=True)
        log_in_page.login_error_alert_is_visible("The email must be a valid")


    @pytest.mark.positive
    def test_login_validate_field_email_uppercase(self, log_in_page, test_user):
        log_in_page.login(email=test_user.email, password=test_user.password)
        log_in_page.user_logged_in_success()

    @pytest.mark.negative
    def test_login_email_not_verified(self, log_in_page, unverified_user):
        log_in_page.login(email=unverified_user.email, password=unverified_user.password)
        log_in_page.login_error_alert_is_visible("You need to verify your email address to access account.")

    @pytest.mark.negative
    def test_login_email_not_registered(self, log_in_page, test_user_data):
        log_in_page.login(email=test_user_data.email, password=test_user_data.password)
        log_in_page.login_error_alert_is_visible("Email or password is incorrect")

    @pytest.mark.negative
    def test_login_invalid_password(self, log_in_page, test_user, test_user_data):
        log_in_page.login(email=test_user.email, password=test_user_data.password)
        log_in_page.login_error_alert_is_visible("Email or password is incorrect")

    @pytest.mark.negative
    def test_login_user_not_verified(self, log_in_page, not_verified_user):
        log_in_page.login(
            email=not_verified_user.email,
            password=not_verified_user.password,
            negative=True
        )
        log_in_page.login_error_alert_is_visible("You need to verify your email address to access account.")