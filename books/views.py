from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book

from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookDeleteSerializer,
    BookUpdateSerializer,
)


class BookViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Instantiates and returns permissions that this view requires.
        """
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated | IsAdminUser]
        elif self.action in ("create", "update", "delete"):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        if self.action in ("update", "partial_update"):
            return BookUpdateSerializer

        if self.action == "delete":
            return BookDeleteSerializer

        return BookSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the books with filters"""
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            author_ids = self._params_to_ints(author)
            queryset = queryset.filter(author__id__in=author_ids)

        return queryset.distinct()

    def perform_create(self, serializer):
        """Check constraints when creations new book"""
        try:
            instance = serializer.save()
            instance.save()
        except ValidationError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                exception=True,
            )
