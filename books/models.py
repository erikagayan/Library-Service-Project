from django.db import models


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
