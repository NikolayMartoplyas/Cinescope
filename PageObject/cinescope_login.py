import allure
from playwright.sync_api import Page, expect
from PageObject.base_page import BasePage
class CinescopeLogin(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}login"
        self.from_title = page.get_by_role("heading", name="Войти")
        self.login_button = page.locator("form").get_by_role("button", name="Войти")
        self.register_button = page.get_by_role("link", name="Зарегистрироваться")

    @allure.step("Заполнение формы автризации")
    def login_form(self, email: str, password: str):
        self.check_element(self.from_title)
        self.enter_email(email)
        self.enter_password(password)
        self.click_element(self.login_button)

    @allure.step("Переход на стрицу входа")
    def open_form_login(self):
        self.open_url(self.url)


    @allure.step("Ожидание перехода на домашнюю страницу")
    def wait_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.url)

    @allure.step("Проверка всплывающего сообщения после редирект")
    def check_allert(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")


