import allure

from resources.user_creds import SuperAdminCreds
from PageObject.cinescope_register import CinescopeRegisterPage
from PageObject.cinescope_login import CinescopeLogin
from faker import Faker
from utils.data_generator import DataGenerator


faker = Faker()

@allure.epic("Тестирование UI")
@allure.story("Тестирование формы регистрации и авторизации")
class TestUI:

    @allure.title("Тестирование формы регистрации")
    def test_register_user(self, page):
        password = DataGenerator.generate_random_password()
        register_page = CinescopeRegisterPage(page)
        register_page.open_form_register()
        register_page.register(
            full_name=DataGenerator.generate_random_full_name(),
            email=DataGenerator.generate_random_email(),
            password= password,
            password_repeat=password
        )
        register_page.make_screenshot_and_attach_to_allure()
        register_page.redirect_to_login()
        register_page.check_allert()

    @allure.title("Тестирование формы авторизации")
    def test_login_user(self, page):
        login = CinescopeLogin(page)
        login.open_form_login()
        login.login_form(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)
        login.make_screenshot_and_attach_to_allure()
        login.wait_redirect_to_home_page()
        login.check_allert()
