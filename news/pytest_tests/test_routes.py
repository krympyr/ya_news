"""Тестирование маршрутов."""
import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from .conftest import URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urls',
    (
        URL.detail,
        URL.home,
        URL.login,
        URL.logout,
        URL.signup,
    )
)
def test_pages_availability_for_anonymous_user(client, news, urls):
    """Доступность страниц анонимному пользователю."""
    response = client.get(urls)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'urls',
    (URL.edit, URL.delete),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, urls, comment, expected_status
):
    """Тест доступа на страницу редактирования и удаления комментария."""
    response = parametrized_client.get(urls)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urls',
    (URL.edit, URL.delete),
)
def test_redirect_for_anonymous_client(client, urls, comment):
    """
    Тест редиректов для анонимного пользователя.

    Для страниц редактирования и удаления чужих комментариев.
    """
    expected_url = f'{URL.login}?next={urls}'
    response = client.get(urls)
    assertRedirects(response, expected_url)
