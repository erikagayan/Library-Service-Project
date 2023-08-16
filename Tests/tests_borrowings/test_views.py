from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from borrowings.models import Borrowing
from books.models import Book
from users.models import User
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com", password="testpassword"
        )
        self.book1 = Book.objects.create(title="Book 1", inventory=3, daily_fee=1)
        self.book2 = Book.objects.create(title="Book 2", inventory=0, daily_fee=2)

        self.borrowing1 = Borrowing.objects.create(
            user=self.user,
            book=self.book1,
            expected_return_date=timezone.now().date() + timedelta(days=7),
        )
        self.borrowing2 = Borrowing.objects.create(
            user=self.user,
            book=self.book2,
            expected_return_date=timezone.now().date() + timedelta(days=7),
        )

        self.client.force_authenticate(user=self.user)

    def test_create_borrowing_with_no_inventory(self):
        data = {
            "book": self.book2.id,
            "expected_return_date": timezone.now().date() + timedelta(days=14),
        }
        response = self.client.post(reverse("borrowing:borrowing-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_return_borrowing(self):
        borrowing_id = self.borrowing1.id
        initial_inventory = self.book1.inventory
        response = self.client.put(
            reverse("borrowing:borrowing-return-borrowing", args=[borrowing_id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_borrowing = Borrowing.objects.get(id=borrowing_id)
        self.assertIsNotNone(updated_borrowing.actual_return_date)

        updated_book1 = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book1.inventory, initial_inventory + 1)

    def test_return_borrowing_already_returned(self):
        borrowing_id = self.borrowing1.id
        self.borrowing1.actual_return_date = timezone.now().date()
        self.borrowing1.save()
        response = self.client.put(
            reverse("borrowing:borrowing-return-borrowing", args=[borrowing_id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.book1.inventory, 3)

    def test_return_borrowing_invalid_borrowing(self):
        response = self.client.put(reverse("borrowing:borrowing-return-borrowing", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_active_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_inactive_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, {"is_active": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_borrowings_by_user_id(self):
        user_id = 1
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, {"user_id": user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
