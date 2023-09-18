from rest_framework import serializers
from borrowings.models import Borrowing
from books.serializers import BookDetailSerializer
from payments.serializers import PaymentSerializer
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(
        source="payments",
        read_only=True,
        many=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment",
        )


class BorrowingListSerializer (BorrowingSerializer):
    payment = serializers.SlugRelatedField(
        source="payments",
        read_only=True,
        many=True,
        slug_field="short_payment_info"
    )
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment"
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    payment = PaymentSerializer(
        source="payments",
        read_only=True,
        many=True
    )
    book = BookDetailSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date")
