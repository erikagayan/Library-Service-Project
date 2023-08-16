from rest_framework.exceptions import ValidationError

from books.models import Book


class UniqueTitleCoverValidator:
    def __call__(self, value):
        title = value.get('title')
        cover = value.get('cover')
        if Book.objects.filter(title=title, cover=cover).exists():
            raise ValidationError(
                "A book with the same title and cover already exists."
            )
