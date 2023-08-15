from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Book


BOOK_URL = reverse("book:book-list")


def detail_url(book_id: int):
    return reverse("book:book-detail", args=[book_id])


def sample_book(**params) -> Book:
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "HARD",
        "inventory": 10,
        "daily_fee": 10.0,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnAuthenticatedBookViesSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = sample_book()

    def test_list_allowed(self) -> None:
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_not_allowed(self) -> None:
        new_book_data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 8.0,
        }
        result_post = self.client.post(BOOK_URL, new_book_data)
        self.assertEqual(result_post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_not_allowed(self) -> None:
        book = self.book
        url = detail_url(book.id)
        partial_data = {"title": "Partial Update"}
        result_patch = self.client.patch(url, partial_data)
        self.assertEqual(result_patch.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_not_allowed(self) -> None:
        book = self.book
        url = detail_url(book.id)
        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
        }
        result_put = self.client.put(url, updated_data)
        self.assertEqual(result_put.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_allowed_required(self) -> None:
        book = self.book
        url = detail_url(book.id)
        result_delete = self.client.delete(url)

        self.assertEqual(result_delete.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminBookApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "password",
            is_staff=True,
        )

        self.book1 = sample_book(title="book1")
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 8.0,
        }

        result = self.client.post(BOOK_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        payload = {
            "title": "Book",
            "author": "Author",
        }

        book_detail_url = detail_url(self.book1.id)
        result = self.client.patch(book_detail_url, payload)

        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_delete_book_not_allowed(self):
        book = self.book1

        url = detail_url(book.id)

        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)


class AuthenticatedBookApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "password",
            is_staff=False,
        )

        self.book = sample_book(title="Doom")
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 8.0,
        }

        result = self.client.post(BOOK_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        payload = {
            "title": "New Book",
            "author": "New Author",
        }

        result = self.client.put(BOOK_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_book_not_allowed(self):
        book = self.book

        url = detail_url(book.id)

        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)
