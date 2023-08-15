from rest_framework import mixins, viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        # if self.action == "create":
        #     return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.expected_return_date and instance.expected_return_date < instance.borrow_date:
            raise serializers.ValidationError("Expected return date cannot be earlier than borrow date.")

        if instance.actual_return_date and instance.actual_return_date < instance.borrow_date:
            raise serializers.ValidationError("Actual return date cannot be earlier than borrow date.")


class CreateBorrowingView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = BorrowingCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
