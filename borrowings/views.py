from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,

)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        if is_active:
            if is_active.lower() == "true/":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false/":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if user.is_staff and user_id:
            user_id = user_id.rstrip("/")
            queryset = queryset.filter(user_id=user_id)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        book = instance.book
        if book.inventory == 0:
            raise serializers.ValidationError("Book inventory is 0.")

        book.inventory -= 1
        book.save()

        instance.user = self.request.user
        instance.save()

        if instance.expected_return_date and instance.expected_return_date < instance.borrow_date:
            raise serializers.ValidationError("Expected return date cannot be earlier than borrow date.")

        if instance.actual_return_date and instance.actual_return_date < instance.borrow_date:
            raise serializers.ValidationError("Actual return date cannot be earlier than borrow date.")
