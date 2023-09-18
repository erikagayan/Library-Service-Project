from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    )

    TYPE_CHOICES = (
        ("PAYMENT", "Payment"),
        ("FINE", "Fine"),
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(
        to=Borrowing,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=80)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["status"]

    def __str__(self):
        return f"{self.type} - {self.status}"

    @property
    def short_payment_info(self):
        return f"{self.status}|{self.type}|{self.money_to_pay} cents"
