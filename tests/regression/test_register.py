import pytest

from test_data.disposable_domains import DISPOSABLE_DOMAINS
from utils.fake_user_data import fake
from test_data.errors.register_errors import RegisterErrors


@pytest.mark.regression
@pytest.mark.register
class TestRegister:
    @pytest.mark.negative
    @pytest.mark.parametrize("domain", DISPOSABLE_DOMAINS, ids=lambda d: d)
    def test_register_disposable_domains(self, domain, sign_up_page):
        sign_up_page.registration(email=fake.email(domain=domain), password=fake.password())
        sign_up_page.register_error_alert_is_visible(RegisterErrors.EMAIL_DISPOSABLE_ERROR)

    @pytest.mark.negative
    def test_email_already_registered(self, sign_up_page, test_user):
        sign_up_page.registration(email=fake.email(), password=fake.password())

