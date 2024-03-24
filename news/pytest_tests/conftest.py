"""Файл конфигурации тестов."""
import pytest
from datetime import datetime, timedelta
from collections import namedtuple
from django.utils import timezone
from django.test.client import Client
from django.conf import settings
from django.urls import reverse
from news.models import News, Comment


FEW_COMMENTS = 5
COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Новый коммнтарий'
PK = 1

URL_NAME = namedtuple(
    'NAME',
    [
        'home',
        'detail',
        'edit',
        'delete',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('news:home'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


@pytest.fixture
def author(django_user_model):
    """Пользователь автор."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Пользователь НЕ автор."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Авторизованный автор."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Авторизованный Не автор."""
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    """Новость."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def pk_news_for_args(news):
    """Возвращаем id новости."""
    return (news.id,)


@pytest.fixture
def comment(news, author):
    """Комментарий для новости."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT
    )
    return comment


@pytest.fixture
def few_comments(news, author):
    """Несколько комментариев для новости."""
    now = timezone.now()
    for index in range(FEW_COMMENTS):
        comments = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )
    comments.created = now + timedelta(days=index)
    comments.save()
    return comments


@pytest.fixture
def all_news():
    """Несколько новостей, но больше отображ кол-ва на странице."""
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def new_comment_text():
    """Текст добавляемого комментария."""
    form_data = {'text': NEW_COMMENT_TEXT}
    return form_data
