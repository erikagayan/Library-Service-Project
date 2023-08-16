from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from books.models import Book
from borrowings.models import Borrowing


class BorrowingModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(email="testuser@example.com", password="testpassword")
        cls.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=35,
            daily_fee=10.99
        )

    def test_borrowing_creation(self):
        borrowing = Borrowing.objects.create(
            expected_return_date="2023-08-15",
            book=self.book,
            user=self.user
        )
        self.assertEqual(str(borrowing), f"{self.user} borrowed {self.book}")

    def test_borrowing_ordering(self):
        borrowing1 = Borrowing.objects.create(
            expected_return_date="2023-08-15",
            book=self.book,
            user=self.user
        )
        borrowing2 = Borrowing.objects.create(
            expected_return_date="2023-08-16",
            book=self.book,
            user=self.user
        )
        borrowing2.borrow_date = borrowing2.borrow_date + timedelta(days=1)
        borrowing2.save()

        self.assertLess(borrowing1.borrow_date, borrowing2.borrow_date)

    def test_actual_return_date_nullable(self):
        borrowing = Borrowing.objects.create(
            expected_return_date="2023-08-15",
            book=self.book,
            user=self.user
        )
        self.assertIsNone(borrowing.actual_return_date)