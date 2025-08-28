import json
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.serializers import BookingCreateSerializer
from db.models import (
    Table, 
    Booking
)


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
            return JsonResponse(booking_serializer.errors, status=409)
    
    date = request.GET.get('date')

    return JsonResponse(
        {"tables": [{"id": i.id, "name": i.name} for i in Table.objects.all()]}
    )
