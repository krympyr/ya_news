"""Тестирование контента."""
import pytest
from http import HTTPStatus
from django.conf import settings
from news.forms import CommentForm
from .conftest import URL


pytestmark = pytest.mark.django_db


def test_news_count(client, all_news):
    """Количесто новостей на гл странице не более 10."""
    response = client.get(URL.home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news):
    """Новости на гл странице отсортированы от свежих к старым."""
    response = client.get(URL.home)
    object_list = response.context['object_list']
    all_dates = [all_news.date for all_news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, few_comments, news):
    """Комментарии отсортированы от старых к свежим."""
    response = client.get(URL.detail)
    assert response.status_code == HTTPStatus.OK
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, news):
    """Форма не передаётся в словаре контекста для анонима."""
    response = client.get(URL.detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    """Форма передаётся в словаре контекста для авториз пользоватля."""
    response = author_client.get(URL.detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
