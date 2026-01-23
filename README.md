### Порядок действий перед выполнением тестов
1) Создать виртуальное окружение командой **.venv\\Scripts\\activate**
2) Из файла **requirements.txt** утсановить библиотеки командой **pip install -r requirements.txt**
2) Cоздать файл .env в корне проекта 
3) Выполнить каманды описанные в файле **.env.example**
4) Тесты для ендпоинта /movies запускаются командой  **pytest tests/api/test_API_movies**
