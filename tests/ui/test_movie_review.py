import allure
import pytest
from playwright.sync_api import expect
from PageObject.page_movie_card import MovieCard
from utils.data_generator import DataGenerator

@pytest.mark.ui
@allure.epic("Тестирование Оставление отзыва на фильм")
class TestReview:

    @allure.title("Оставить отзыв на фильм")
    def test_movie_review(self, delete_review):
        page = delete_review
        with allure.step("Создание экземпляров класса"):
            review = DataGenerator.review()
            card_movie = MovieCard(page)

        with allure.step("Оставление отзыва"):
            card_movie.write_review(review)
            card_movie.click_button_send()
            expect(page.get_by_text(review)).to_be_visible()
            card_movie.make_screenshot()







