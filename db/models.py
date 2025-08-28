from django.db import models
from django.db.models import Index

class Table(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
      db_table = 'tables'

    def __str__(self) -> str:
        return self.name


class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateTimeField()
    client_name = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'bookings'
        indexes = (
            Index(fields=['date'], name='date_index'),
        )

    def __str__(self) -> str:
        return f"{self.client_name} - {self.table} - {self.date}"
