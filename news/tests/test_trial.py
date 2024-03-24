from django.test import TestCase
from news.models import News
from unittest import skip

# Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
@skip("Пропуск_триал_тестов")
class TestNews(TestCase):

    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'
    # В методе класса setUpTestData создаём тестовые объекты.
    # Оборачиваем метод соответствующим декоратором.    
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
        )

    def test_successful_creation(self):
        news_count = News.objects.count()
        self.assertEqual(news_count, 1)

    def test_title(self):
        # Сравним свойство объекта и ожидаемое значение.
        self.assertEqual(self.news.title, self.TITLE) 

@skip("Пропуск_триал_тестов")
class Test(TestCase):

    def test_example_success(self):
        self.assertTrue(True)  # Этот тест всегда будет проходить успешно

@skip("Пропуск_триал_тестов")
class YetAnotherTest(TestCase):

    def test_example_fails(self):
        self.assertTrue(False)  # Этот тест всегда будет проваливаться.