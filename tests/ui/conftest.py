import allure
import pytest
from playwright.sync_api import sync_playwright, expect

from PageObject.all_movies import AllMovies
from PageObject.page_movie_card import MovieCard
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

@pytest.fixture(scope="function")
def delete_review(login_super_admin):
    """Удаление отзыва в фильме"""
    page = login_super_admin
    with allure.step("Создание экземпляров класса"):
        card_movie = MovieCard(page)
        page_movies = AllMovies(page)

    with allure.step("Выбор фильма"):
        page_movies.go_to_all_movies()
        page_movies.select_filter_location()
        page_movies.select_filter_genre()
        page_movies.select_sorting()
        page_movies.click_button_details()

    with allure.step("Проверка видимости поля для отзыва"):
        check_text = card_movie.check_feedback_field()
        if not check_text:
            card_movie.delete_review()
            expect(card_movie.review_field).not_to_be_visible()

        yield page