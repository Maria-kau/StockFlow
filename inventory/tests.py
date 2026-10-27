
from rest_framework import serializers
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from inventory.serializers import StockMovementSerializer
from inventory.models import StockMovement
from products.models import Product


class StockMovementSerializerTests(TestCase):

    def test_validate_quantity_zero(self):
        serializer = StockMovementSerializer()

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_quantity(0)

    def test_validate_valid_quantity(self):
        serializer = StockMovementSerializer()

        result = serializer.validate_quantity(5)

        self.assertEqual(result, 5)

    def test_validate_quantity_negative(self):
        serializer = StockMovementSerializer()

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_quantity(-8)


class StockEntryAPITests(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Teclado",
            description="Teclado mecânico",
            price="150.00",
            stock=10,
        )

    def test_stock_entry_success(self):
        url = reverse("stock-entry")

        data = {
            "product_id": self.product.id,
            "quantity": 5,
        }

        response = self.client.post(url, data, format="json")

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.product.stock, 15)

        self.assertEqual(
            StockMovement.objects.filter(
                product=self.product,
                movement_type="IN",
                quantity=5,
            ).count(),
            1,
        )

    def test_stock_exit_success(self):
        url = reverse("stock-exit")

        data = {
            "product_id": self.product.id,
            "quantity": 5,
        }

        response = self.client.post(url, data, format="json")

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.stock, 5)

        self.assertEqual(
            StockMovement.objects.filter(
                product=self.product,
                movement_type="OUT",
                quantity=5,
            ).count(),
            1,
        )

    
    def test_movement_history_success(self):
        StockMovement.objects.create(
            product=self.product,
            movement_type="IN",
            quantity=5,
        )

        url = reverse("movement-history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["movement_type"], "IN")
        self.assertEqual(response.data[0]["quantity"], 5)
