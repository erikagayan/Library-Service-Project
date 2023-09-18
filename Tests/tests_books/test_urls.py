from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "password",
            is_staff=True,
        )

        self.client.force_authenticate(self.user)
        self.book_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "5.00",
        }
        self.book = Book.objects.create(**self.book_data)

    def test_list_books(self):
        response = self.client.get(reverse("book:book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        response = self.client.get(reverse("book:book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book_data["title"])

    def test_create_book(self):
        new_book_data = {
            "title": "New Book",
            "author": "Jane Smith",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": "3.00",
        }
        response = self.client.post(reverse("book:book-list"), new_book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        updated_data = {
            "title": "Updated Book Title",
            "inventory": 15,
        }
        response = self.client.patch(reverse("book:book-detail", args=[self.book.id]), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, updated_data["title"])
        self.assertEqual(self.book.inventory, updated_data["inventory"])

    def test_delete_book(self):
        response = self.client.delete(reverse("book:book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
