import datetime
from django.utils import timezone
from rest_framework import mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,

)
from payments.utils import payment_helper


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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
        instance = serializer.validated_data

        book = instance["book"]
        if book.inventory == 0:
            raise serializers.ValidationError(
                "Book inventory is 0. Cannot borrow the book."
            )

        book.inventory -= 1
        book.save()

        if (
                instance["expected_return_date"]
                and instance["expected_return_date"]
                < datetime.datetime.now().date()
        ):
            raise serializers.ValidationError(
                "Expected return date cannot be earlier than borrow date."
            )

        instance = serializer.save(user=self.request.user)
        instance.save()
        payment_helper(instance.id)

    @action(detail=True, methods=["put"])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        serializer = BorrowingDetailSerializer(borrowing)

        return Response(serializer.data)
