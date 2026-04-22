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
        expect(self.from_title).to_be_visible(timeout=10000)
        self.enter_email(email)
        self.enter_password(password)
        self.login_button.click()

    @allure.step("Переход на стрицу входа")
    def open_form_login(self):
        self.page.goto(self.url)


    @allure.step("Ожидание перехода на домашнюю страницу")
    def wait_redirect_to_home_page(self):
        self.page.wait_for_url(f"{self.base_url}", timeout=10000)  # Ожидание загрузки домашней страницы
        assert self.page.url == f"{self.base_url}", "Редирект на домашнюю старницу не произошел"

    @allure.step("Проверка всплывающего сообщения после редирект")
    def check_allert(self):
        # Проверка появления алерта с текстом "Вы вошли в аккаунт"
        notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
        notification_locator.wait_for(state="visible")  # Ждем появления элемента
        assert notification_locator.is_visible(), "Уведомление не появилось"

        # Ожидание исчезновения алерта
        notification_locator.wait_for(state="hidden", timeout=10000)  # Ждем, пока алерт исчезнет
        assert notification_locator.is_visible() == False, "Уведомление исчезло"


