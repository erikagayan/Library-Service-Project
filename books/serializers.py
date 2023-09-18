from rest_framework import serializers
from books.models import Book
from books.validators import UniqueTitleCoverValidator


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")
        validators = [UniqueTitleCoverValidator()]


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover",)


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookUpdateSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookDeleteSerializer(BookSerializer):
    class Meta:
        fields = ("id",)
