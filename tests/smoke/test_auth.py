import pytest


@pytest.mark.auth
class TestAuth:

    @pytest.mark.smoke
    def test_authorisation_with_email(self, test_user, log_in_page):
        log_in_page.login(test_user.email, test_user.password)

        expected_url = "https://thegoodocs.com/"
        log_in_page.wait_for_url(expected_url)

        assert log_in_page.get_current_url() == expected_url

    @pytest.mark.smoke
    def test_registration_with_email(self, sign_up_page, registration_user, mail_service):
        mail_service.delete_all_emails()

        sign_up_page.registration(registration_user.email, registration_user.password)

        activation_url = mail_service.verification_link(timeout_seconds=30)

        assert activation_url != "", "Посилання не прийшло поштою"

        sign_up_page.navigate_to(activation_url)
        sign_up_page.header.verify_is_logged_in()