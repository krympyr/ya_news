"""Тестирование логики."""
import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from .conftest import URL, COMMENT_TEXT, NEW_COMMENT_TEXT


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, new_comment_text):
    """Анонимный пользователь не может создать комментарий."""
    expected_comments = Comment.objects.count()
    client.post(URL.detail, data=new_comment_text)
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments


def test_user_can_create_comment(
        author,
        author_client,
        news,
        new_comment_text):
    """Пользователь может создать комментарий."""
    expected_comments = Comment.objects.count() + 1
    response = author_client.post(URL.detail, data=new_comment_text)
    assertRedirects(response, f'{URL.detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments
    comment = Comment.objects.get()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'bad_word',
    (BAD_WORDS),
)
def test_user_cant_use_bad_words(author_client, bad_word, news):
    """Пользователь не может использовать запрещённые слова в комментариях."""
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, еще текст'}
    response = author_client.post(URL.detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, comment):
    """Автор может удалить свой комментарий."""
    expected_comments = Comment.objects.count() - 1
    url_to_comments = URL.detail + '#comments'
    response = author_client.delete(URL.delete)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments


def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    """Пользователь не может удалить чужой комментарий."""
    expected_comments = Comment.objects.count()
    response = not_author_client.delete(URL.delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments


def test_author_can_edit_comment(
        author_client,
        comment,
        new_comment_text):
    """Автор может редактировать свой комментарий."""
    url_to_comments = URL.detail + '#comments'
    response = author_client.post(URL.edit, data=new_comment_text)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        comment,
        new_comment_text):
    """Пользователь не может редактировать чужой комментарий."""
    response = not_author_client.post(URL.edit, data=new_comment_text)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
