from books.models import Book
from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookUpdateSerializer,
    BookDeleteSerializer
)
from django.test import TestCase
from decimal import Decimal


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 1.5
        }

    def test_valid_book_serializer(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_book_serializer_missing_fields(self):
        invalid_data = self.book_data.copy()
        invalid_data.pop("title")
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_unique_title_cover_validator(self):
        existing_book = Book.objects.create(**self.book_data)
        serializer = BookSerializer(data=self.book_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_valid_book_serializer_with_partial_data(self):
        partial_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": 2.0
        }
        serializer = BookSerializer(data=partial_data)
        self.assertTrue(serializer.is_valid())


class BookListSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "9.99",
        }

        cls.book = Book.objects.create(**cls.book_data)

    def test_book_list_serializer_valid_data(self):
        serializer = BookListSerializer(self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_list_serializer_fields(self):
        serializer = BookListSerializer()
        self.assertEqual(
            serializer.Meta.fields, ("id", "title", "author", "cover")
        )


class BookDetailSerializerTest(TestCase):
    def test_valid_data(self):
        valid_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "5.00"
        }
        serializer = BookDetailSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_field(self):
        invalid_data = {
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "5.00"
        }
        serializer = BookDetailSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_invalid_choice_field(self):
        invalid_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "INVALID_COVER",  # This is not a valid choice
            "inventory": 10,
            "daily_fee": "5.00"
        }
        serializer = BookDetailSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cover", serializer.errors)

    def test_invalid_daily_fee(self):
        invalid_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "invalid_fee"  # This should be a valid decimal
        }
        serializer = BookDetailSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("daily_fee", serializer.errors)


class BookUpdateSerializerTest(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "9.99",
        }
        self.book = Book.objects.create(**self.book_data)
        self.serializer = BookUpdateSerializer(instance=self.book)

    def test_valid_serializer_data(self):
        updated_data = {
            "title": "Updated Book Title",
            "author": "Jane Smith",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": "12.99",
        }

        serializer = BookUpdateSerializer(instance=self.book, data=updated_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], updated_data["title"])
        self.assertEqual(serializer.validated_data["author"], updated_data["author"])
        self.assertEqual(serializer.validated_data["cover"], updated_data["cover"])
        self.assertEqual(serializer.validated_data["inventory"], updated_data["inventory"])
        self.assertEqual(serializer.validated_data["daily_fee"], Decimal(updated_data["daily_fee"]))

    def test_invalid_serializer_data(self):
        invalid_data = {
            "title": "",
            "author": "New Author",
        }

        serializer = BookUpdateSerializer(instance=self.book, data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_partial_update_serializer(self):
        partial_data = {
            "author": "Updated Author",
        }

        serializer = BookUpdateSerializer(instance=self.book, data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.book.refresh_from_db()

        self.assertEqual(self.book.author, partial_data["author"])

        # Check that other fields remain unchanged
        self.assertEqual(self.book.title, "Sample Book")
        self.assertEqual(self.book.cover, "HARD")
        self.assertEqual(self.book.inventory, 10)
        self.assertEqual(self.book.daily_fee, Decimal("9.99"))

    def test_update_serializer_with_empty_data(self):
        original_data = {
            "title": self.book.title,
            "author": self.book.author,
            "cover": self.book.cover,
            "inventory": self.book.inventory,
            "daily_fee": Decimal(self.book.daily_fee),
        }

        serializer = BookUpdateSerializer(instance=self.book, data={}, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.book.refresh_from_db()

        # Check that all fields remain unchanged
        self.assertEqual(self.book.title, original_data["title"])
        self.assertEqual(self.book.author, original_data["author"])
        self.assertEqual(self.book.cover, original_data["cover"])
        self.assertEqual(self.book.inventory, original_data["inventory"])
        self.assertEqual(self.book.daily_fee, original_data["daily_fee"])
