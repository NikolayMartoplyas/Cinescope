import allure
from playwright.sync_api import Page

class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://dev-cinescope.coconutqa.ru/"
        self.home_button = page.get_by_role('link', name='Cinescope')
        self.all_movies = page.get_by_role("link", name="Все фильмы")
        self.email = page.get_by_role("textbox", name="Email")
        self.password = page.get_by_role("textbox", name="Пароль", exact=True)

    @allure.step("переход на глаыную страницу")
    def go_to_home_page(self):
        self.home_button.click()
        self.page.wait_for_url(self.base_url)

    @allure.step("Переход ко всем фильмам")
    def go_to_all_movies(self):
        self.all_movies.click()
        self.page.wait_for_url(f"{self.base_url}movies")

    @allure.step("Ввод email")
    def enter_email(self, email: str):
        self.email.fill(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str):
        self.password.fill(password)

    @allure.step("Прикрепляем скриншот страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True) #full_page = True для скриншота всей страницы

        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)