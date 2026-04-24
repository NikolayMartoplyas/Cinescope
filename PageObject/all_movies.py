import allure

from PageObject.base_page import BasePage
from playwright.sync_api import Page

class AllMovies(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}movies"
        self.filter_place = page.get_by_role("combobox").first
        self.filter_genre = page.get_by_role("combobox").nth(1)
        self.filter_created = page.get_by_role("combobox").filter(has_text="Создано")
        self.selected_location = page.get_by_text("MSK")
        self.selected_genre = page.get_by_text("Комедия")
        self.selected_sorting = page.get_by_text("Новые")
        self.card_movie = page.locator(".rounded-xl.border.bg-card").first


    @allure.step("Выибор фильтра место")
    def select_filter_location(self):
        self.click_element(self.filter_place)
        self.click_element(self.selected_location)

    @allure.step("Выбираем фильтр жанр")
    def select_filter_genre(self):
        self.click_element(self.filter_genre)
        self.click_element(self.selected_genre)

    @allure.step("Выбираем сортировку")
    def select_sorting(self):
        self.click_element(self.filter_created)
        self.click_element(self.selected_sorting)

    @allure.step("Нажимаем кнопку 'Подробнее' на карточке фильма")
    def click_button_details(self):
        self.card_movie.get_by_role("button", name="Подробнее").click()


