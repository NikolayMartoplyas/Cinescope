from asyncio import timeout
from time import sleep

import allure
from playwright.sync_api import expect

from PageObject.all_movies import AllMovies
from PageObject.page_movie_card import MovieCard
from PageObject.page_movie_card import MovieCard


@allure.epic("Тестирование Оставление отзыва на фильм")
class TestReview:

    @allure.title("Оставить отзыв на фильм")
    def test_movie_reviev(self, login_super_admin):
        page = login_super_admin
        with allure.step("Создание экземпляров класса"):
            card_movie = MovieCard(page)
            page_movies = AllMovies(page)
            review = MovieCard.review()

        with allure.step("Выбор фильма"):
            page_movies.go_to_all_movies()
            page_movies.select_filter_location()
            page_movies.select_filter_genre()
            page_movies.select_sorting()
            page_movies.click_button_details()

        with allure.step("Оставление отзыва"):
            check_field = card_movie.check_feedback_field()
            if check_field == False:
                card_movie.delete_review()
                expect(page.get_by_text(review)).not_to_be_visible()
            else:
                card_movie.write_review(review)
                card_movie.click_button_send()
                expect(page.get_by_text(review)).to_be_visible()
                card_movie.make_screenshot()







