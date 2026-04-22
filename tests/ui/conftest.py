import pytest
from playwright.sync_api import sync_playwright
from common.tools import Tools
from utils.data_generator import DataGenerator
from PageObject.cinescope_register import CinescopeRegisterPage
from PageObject.cinescope_login import CinescopeLogin
from PageObject.profile import PageProfile
from resources.user_creds import SuperAdminCreds

DEFAULT_TIMEOUT = 3000
@pytest.fixture(scope="session")
def browser():
    """Запуск браузера"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    """Создание контекста"""
    context = browser.new_context()
    context.tracing.start(sources=True, snapshots=True, screenshots=True)
    context.set_default_timeout(DEFAULT_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir("playwright_trace", log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Создание страницы"""
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def register_user(page):
    """Регистрация пользователя"""
    full_name = DataGenerator.generate_random_full_name()
    email = DataGenerator.generate_random_email()
    password = DataGenerator.generate_random_password()
    regisre_page = CinescopeRegisterPage(page)
    regisre_page.open_form_register()
    regisre_page.register(full_name, email, password=password, password_repeat=password)
    yield {"email": email, "password": password}

@pytest.fixture(scope="function")
def login_super_admin(page):
    """Авторизация супер админа"""
    login_page = CinescopeLogin(page)
    login_page.open_form_login()
    login_page.login_form(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)
    login_page.wait_redirect_to_home_page()
    login_page.check_allert()
    yield page
    profile = PageProfile(page)
    profile.open_page_profile()
    profile.logout()
    profile.check_logout()
