import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.utils import get_start_end_dates_for_filter_bookings
from api.serializers import BookingCreateSerializer
from db.models import Table


def index(request):
    return render(request, "index.html", {"data": 123})


@csrf_exempt
def booking(request):
    """
    GET: return all tables
    GET + querry param: returns a list of available tables for a given date ± 2 hours. "date": "01.07.2023T20:00"

    POST: Create new booking
    """

    if request.method == "POST":
        """Create new booking"""
        data = json.loads(request.body.decode("utf-8"))

        booking_serializer = BookingCreateSerializer(data=data)
  
        if booking_serializer.is_valid():

          booking_serializer.save()
          return JsonResponse(booking_serializer.data, status=201)

        else:
            print(booking_serializer.errors)

            return JsonResponse(booking_serializer.errors, status=409)
    
    booking_date = request.GET.get('date')
    available_tables = Table.objects.all().values('id', 'name')
 
    if not booking_date:
       return JsonResponse({"tables": list(available_tables)}, status=200)

    booking_date_obj = datetime.strptime(booking_date, "%d.%m.%YT%H:%M")
    start, end = get_start_end_dates_for_filter_bookings(date=booking_date_obj, hours_diff=1)

    available_tables = (
      available_tables
      .exclude(bookings__date__gte=start, bookings__date__lte=end)
      .distinct()
    )
    
    return JsonResponse({"tables": list(available_tables)}, status=200)
