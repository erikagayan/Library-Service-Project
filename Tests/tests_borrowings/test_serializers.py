from django.test import TestCase
from borrowings.models import Borrowing
from books.models import Book
from users.models import User
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="testuser@example.com", password="testpassword")
        cls.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=35,
            daily_fee=10.99
        )
        cls.borrowing = Borrowing.objects.create(
            user=cls.user,
            book=cls.book,
            borrow_date="2023-08-16",
            expected_return_date="2023-08-18",
        )

    def test_borrowing_serializer(self):
        serializer = BorrowingSerializer(instance=self.borrowing)
        print(serializer.data)
        expected_data = {
            "id": 1,
            "borrow_date": "2023-08-16",
            "expected_return_date": "2023-08-18",
            "actual_return_date": None,
            "book": 1,
            "user": 1,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrowing_list_serializer(self):
        serializer = BorrowingListSerializer(instance=self.borrowing)
        expected_data = {
            "id": 1,
            "borrow_date": "2023-08-16",
            "expected_return_date": "2023-08-18",
            "actual_return_date": None,
            "book": self.book.title,
            "user": self.user.email,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrowing_detail_serializer(self):
        serializer = BorrowingDetailSerializer(instance=self.borrowing)
        expected_data = {
            "borrow_date": "2023-08-16",
            "expected_return_date": "2023-08-18",
            "actual_return_date": None,
            "book": {
                "id": 1,
                "title": "Test Book",
                "author": "Test Author",
                "cover": "HARD",
                "inventory": 35,
                "daily_fee": "10.99"
            },
            "user": {
                "id": 1,
                "email": "testuser@example.com",
                "is_staff": False
            },
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrowing_create_serializer(self):
        data = {
            "book": self.book.id,
            "expected_return_date": "2023-08-20",
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        borrowing = serializer.save(user=self.user)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)