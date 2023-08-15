from django.conf import settings
from django.db import models
from django.utils import timezone
from pytz import utc
from django.core.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.user} borrowed {self.book}"
