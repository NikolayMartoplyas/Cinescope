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
        self.details_button = page.locator("a[href='/movies/40790'] button")


    @allure.step("Выибор фильтра место")
    def select_filter_location(self):
        self.filter_place.click()
        self.selected_location.click()

    @allure.step("Выбираем фильтр жанр")
    def select_filter_genre(self):
        self.filter_genre.click()
        self.selected_genre.click()

    @allure.step("Выбираем сортировку")
    def select_sorting(self):
        self.filter_created.click()
        self.selected_sorting.click()

    @allure.step("Нажимаем кнопку 'Подробнее' на карточке фильма")
    def click_button_details(self):
        self.details_button.click()


