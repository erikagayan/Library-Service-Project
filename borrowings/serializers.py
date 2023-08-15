from django.db import transaction
from rest_framework import serializers
from borrowings.models import Borrowing
from books.serializers import BookDetailSerializer
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingListSerializer (BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("book",)

    def validate(self, book):
        if book.inventory <= 0:
            raise serializers.ValidationError("Book inventory is empty.")
        return book

    def create(self, validated_data):
        # validated_data["user"] = self.context["request"].user
        #
        # book = validated_data["book"]
        # book.inventory -= 1
        # book.save()
        #
        # return super().create(validated_data)
        user = self.context["request"].user
        book = validated_data["book"]

        with transaction.atomic():
            borrowing = Borrowing.objects.create(user=user, book=book)
            book.inventory -= 1
            book.save()

        return borrowing
