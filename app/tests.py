import json
from django.test import TestCase
from django.urls import reverse
from db.models import Table


class BookingViewTests(TestCase):
    def setUp(self):
        self.url = reverse("booking")
    
        Table.objects.create(name="Table 1")
        Table.objects.create(name="Table 2")

    def test_get_all_tables_without_date(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("tables", data)
        self.assertEqual(len(data["tables"]), 2)

    def test_get_tables_with_date(self):
        response = self.client.get(self.url, {"date": "28.08.2025T18:00"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("tables", response.json())

    def test_post_missing_required_fields(self):
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)
        errors = response.json()
        self.assertIn("client_name", errors)
        self.assertIn("client_phone", errors)
        self.assertIn("date", errors)
        self.assertIn("table", errors)

    def test_post_create_booking_success(self):
        table = Table.objects.first()
        payload = {
            "client_name": "Alex",
            "client_phone": "0931234567",
            "date": "28.08.2025T18:00",
            "table": table.id
        }
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["client_name"], "Alex")
        self.assertEqual(data["table"], table.id)
