from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from db.models import *


def index(request):
    return render(request, "index.html", {"data": 123})


@csrf_exempt
def booking(request):
    """
    GET: return all tables
    GET+params: returns a list of available tables for a given date. "date": "01.07.2023T20:00"

    POST: Create new booking
    """
    if request.method == "POST":
        """Create new booking"""
        return JsonResponse(
            {
                "client_name": "Alex",
                "client_phone": "0931234567",
                "date": "29.06.2023T20:00",
                "table": 2,
            }
        )
    return JsonResponse(
        {"tables": [{"id": i.id, "name": i.name} for i in Table.objects.all()]}
    )
