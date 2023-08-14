from django.db import models

from users.models import User


class Book(models.Model):
    COVER_CHOICES = (
        ('HARD', 'Hard Cover'),
        ('SOFT', 'Soft Cover'),
    )

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.user} borrowed {self.book}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )

    TYPE_CHOICES = (
        ('PAYMENT', 'Payment'),
        ('FINE', 'Fine'),
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField()
    session_id = models.CharField(max_length=50)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["status"]

    def __str__(self):
        return f"{self.type} - {self.status}"
