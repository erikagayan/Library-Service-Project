from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from books.models import Book


class BookViewsSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_put(self, serializer):
        instance = serializer.save()
        instance.inventory += 1
        instance.save()

    def perform_destroy(self, instance):
        instance.inventory -= 1
        instance.save()

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
