import os
from dataclasses import dataclass
import pytest
from playwright.sync_api import Page, BrowserContext
from faker import Faker


from pages.category_page import CategoryPage
from pages.auth_page import AuthPage
from pages.template_page import TemplatePage
from pages.all_templates_page import AllTemplatesPage
from utils.get_required_env import get_required_env
from utils.api_requests import authorization, create_user, delete_user, delete_user_by_email
from utils.mail_imap import MailIMAP

fk = Faker()


@dataclass
class UserCredentials:
    email: str
    password: str
    id: int | str | None = None


# --- Повне блокування реклами (Google Vignette, AdSense, Analytics) ---
@pytest.fixture(autouse=True)
def block_google_ads_completely(request, context: BrowserContext, page: Page):
    if request.node.get_closest_marker("ads"):
        yield  # реклама потрібна, нічого не блокуємо
        return
    """
    Примусово блокує завантаження рекламних скриптів Google AdSense,
    що запобігає появі оверлеїв типу #google_vignette.
    """
    # 1. Точні шаблони для блокування рекламних серверів та скриптів
    ad_patterns = [
        "**/*googlesyndication.com/**",
        "**/*googleadservices.com/**",
        "**/*google-analytics.com/**",
        "**/pagead/js/adsbygoogle.js*",
        "**/show_ads_impl*.js*",
        "**/*pagead2.googlesyndication*",
        "**/*tpc.googlesyndication*",
    ]

    for pattern in ad_patterns:
        context.route(pattern, lambda route: route.abort())

    # 2. Перевизначення JS-об'єкта adsbygoogle та приховування можливих залишків у DOM
    page.add_init_script("""
        // Заглушка для об'єкта Google Ads, щоб скрипти сайту не викликали помилок
        Object.defineProperty(window, 'adsbygoogle', {
            get: () => [],
            set: () => {}
        });

        // Видалення хешу #google_vignette з URL
        if (window.location.hash.includes('google_vignette')) {
            history.replaceState("", document.title, window.location.pathname + window.location.search);
        }

        // Примусові CSS стилі для приховування будь-яких рекламних контейнерів
        const style = document.createElement('style');
        style.innerHTML = `
            #google_vignette,
            .google-vignette-test,
            ins.adsbygoogle,
            iframe[src*="google"],
            div[id*="google_ads_iframe"] {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
            }
            body {
                overflow: auto !important;
            }
        `;
        document.head.appendChild(style);
    """)

    yield


# --- Сторінки (Page Objects) ---
@pytest.fixture
def category_page(page: Page) -> CategoryPage:
    cp = CategoryPage(page)
    cp.navigate_to("https://thegoodocs.com/freebies/book-templates/")
    return cp


@pytest.fixture
def log_in_page(page: Page) -> AuthPage:
    ap = AuthPage(page)
    ap.navigate_to("https://thegoodocs.com/personal/login/")
    return ap


@pytest.fixture
def sign_up_page(page: Page) -> AuthPage:
    ap = AuthPage(page)
    ap.navigate_to("https://thegoodocs.com/personal/login/?sign-up=true")
    return ap

@pytest.fixture
def all_templates_page(page: Page) -> AllTemplatesPage:
    atp = AllTemplatesPage(page)
    atp.navigate_to("https://thegoodocs.com/all-templates/")
    return atp


@pytest.fixture
def template_page_new_design(page:Page) -> TemplatePage:
    tp = TemplatePage(page)
    tp.navigate_to("https://thegoodocs.com/book-templates/stylish-novel-book-free-google-docs-template.php")
    return tp

@pytest.fixture
def template_page_old_design(page:Page) -> TemplatePage:
    tp = TemplatePage(page)
    tp.navigate_to("https://thegoodocs.com/schedules/weekly-hourly-planner-schedule-template.php")
    return tp


# --- Користувачі та допоміжні фікстури ---
@pytest.fixture
def test_user(auth_admin):
    test_email = fk.email(safe=True, domain="kdteam.test")
    print(test_email)
    test_pass = fk.password(length=6)
    test_user = create_user(
        auth_admin,
        apikey=get_required_env("API_KEY"),
        email=test_email,
        password=test_pass
    )
    test_user_id = test_user["data"]["id"]
    user_data = UserCredentials(
        email=test_email,
        password=test_pass,
        id=test_user_id
    )
    yield user_data
    resp = delete_user(
        auth_admin,
        apikey=get_required_env("API_KEY"),
        user_id=test_user_id
    )
    print(resp)


@pytest.fixture
def registration_user(auth_admin) -> UserCredentials:
    """
    Бере email з ENV, ґенерує пароль через Faker.
    Після завершення тесту автоматично видаляє створеного користувача.
    """
    user_email = os.getenv("TEST_USER_EMAIL_REGISTRATION")
    user_password = fk.password(length=6)

    user = UserCredentials(email=user_email, password=user_password)

    # 1. Передаємо дані у тест
    yield user

    # 2. TEARDOWN: спрацьовує ЗАВЖДИ після тесту (PASS чи FAIL)
    try:
        # Якщо у вас є ID або ви можете отримати його за email/видалити за email:
        delete_user_by_email(
            access_token=auth_admin,
            apikey=get_required_env("API_KEY"),
            email=user.email
        )
        print(f"\n[Teardown] Користувача {user.email} успішно видалено.")
    except Exception as e:
        print(f"\n[Teardown Error] Не вдалося видалити користувача {user.email}: {e}")


@pytest.fixture
def admin_credential():
    return {
        "apikey": get_required_env("API_KEY"),
        "email": get_required_env("ADMIN_EMAIL"),
        "password": get_required_env("ADMIN_PASSWORD"),
    }

@pytest.fixture
def auth_credential(auth_admin):
    return {
        "access_token": auth_admin,
        "api_key":  get_required_env("API_KEY")
    }


@pytest.fixture
def auth_admin(admin_credential):
    return authorization(**admin_credential)["data"]["access_token"]


@pytest.fixture
def mail_service() -> MailIMAP:
    return MailIMAP()