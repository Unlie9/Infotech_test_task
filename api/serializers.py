from datetime import timedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from db.models import Table, Booking
from app.utils import get_start_end_dates_for_filter_bookings



class BookingCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(input_formats=['%d.%m.%YT%H:%M'])

    class Meta:
        model = Booking
        fields = (
            'table',
            'date',
            'client_name',
            'client_phone'
        )

    def create(self, data):
        print(data)
        return super().create(data)
    
    def validate(self, data):
        self.validate_table_on_book_date(data)

        return data
    
    def validate_table_on_book_date(self, data):
        table = data.get("table")
        date = data.get("date")
        start, end = get_start_end_dates_for_filter_bookings(date=date, hours_diff=1)

        table_booking_exists = table.bookings.filter(date__gte=start, date__lte=end).first()
        if table_booking_exists:
          raise ValidationError('That table already booked')

        return super().validate(data)