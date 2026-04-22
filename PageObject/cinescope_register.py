import allure
from playwright.sync_api import Page
from PageObject.base_page import BasePage
class CinescopeRegisterPage(BasePage):
    """
    Класс для работы с формой регистроации для UI тестов
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}register"
        # В конструкторе сразу создаем локаторы
        self.form_title = page.get_by_role("heading", name="Регистрация")
        self.full_name = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.password_repeat = page.get_by_role("textbox", name="Повторите пароль")
        self.button_register =  page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = page.get_by_role("link", name="Войти")

    @allure.step("Переход на форму регистрации")
    def open_form_register(self):
        self.page.goto(self.url)

    @allure.step("Ввод в поле ФИО")
    def enter_full_name(self, full_name: str):
        self.full_name.fill(full_name)

    @allure.step("Ввод подтверждение пароля")
    def enter_password_repeat(self, password_repeat: str):
        self.password_repeat.fill(password_repeat)

    @allure.step("Нажать на кнопку Зарегистрироватся")
    def click_register_button(self):
        self.button_register.click()

    @allure.step("Нажать на кнопку Войти")
    def click_button_Login(self):
        self.sign_button.click()
        self.page.wait_for_url(f"{self.base_url}login")

    @allure.step("Полная форма регистрации")
    def register(self, full_name: str, email: str, password: str, password_repeat: str):
        self.form_title.is_visible(timeout="5000")
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_password_repeat(password_repeat)
        self.click_register_button()

    @allure.step("Переход на страницу авторизации")
    def redirect_to_login(self):
        self.page.wait_for_url(f"{self.base_url}login")
        assert self.page.url == f"{self.base_url}login", "URL не совпадает"

    @allure.step("Проверка всплывающего сообщения после редиректа")
    def check_allert(self):

        # Проверка появления алерта с текстом "Подтвердите свою почту"
        notification_locator = self.page.get_by_text("Подтвердите свою почту")
        notification_locator.wait_for(state="visible")
        assert notification_locator.is_visible(), "Уведомление не появилось"
        notification_locator.wait_for(state="hidden", timeout=8000)  # Ждем, пока алерт исчезнет
        assert notification_locator.is_visible() == False, "Уведомление исчезло"