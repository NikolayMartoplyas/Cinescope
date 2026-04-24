import allure
from playwright.sync_api import Page
from PageObject.page_actions import PageActions

class BasePage(PageActions):

    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "https://dev-cinescope.coconutqa.ru/"
        self.home_button = page.get_by_role('link', name='Cinescope')
        self.all_movies = page.get_by_role("link", name="Все фильмы")
        self.email = page.get_by_role("textbox", name="Email")
        self.password = page.get_by_role("textbox", name="Пароль", exact=True)

    @allure.step("переход на глаыную страницу")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.base_url)

    @allure.step("Переход ко всем фильмам")
    def go_to_all_movies(self):
        self.click_element(self.all_movies)
        self.wait_redirect_for_url(f"{self.base_url}movies")

    @allure.step("Ввод email")
    def enter_email(self, email: str):
        self.enter_text_to_element(self.email, email)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str):
        self.enter_text_to_element(self.password, password)

    @allure.step("Прикрепляем скриншот страницы")
    def make_screenshot(self):
        self.make_screenshot_and_attach_to_allure()