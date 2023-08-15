from rest_framework import mixins, viewsets, serializers
from borrowings.models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book", "user")

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.expected_return_date and instance.expected_return_date < instance.borrow_date:
            raise serializers.ValidationError("Expected return date cannot be earlier than borrow date.")

        if instance.actual_return_date and instance.actual_return_date < instance.borrow_date:
            raise serializers.ValidationError("Actual return date cannot be earlier than borrow date.")
