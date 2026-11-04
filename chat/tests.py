from decimal import Decimal

from django.test import TestCase

from .models import Item
from .tools import change_price_percent, check_stock, list_items


class InventoryToolTests(TestCase):
    """Tests for the inventory tools. They never call Gemini."""

    def setUp(self):
        Item.objects.create(name="Chocolate bar", quantity=40, price=Decimal("3.00"))

    def test_check_stock_returns_quantity_and_price(self):
        result = check_stock("chocolate bar")
        self.assertEqual(result["quantity"], 40)
        self.assertEqual(result["price"], 3.0)

    def test_check_stock_unknown_item(self):
        self.assertIn("error", check_stock("unicorn"))

    def test_list_items(self):
        self.assertEqual(len(list_items()["items"]), 1)

    def test_change_price_percent(self):
        result = change_price_percent("Chocolate bar", 10)
        self.assertAlmostEqual(result["new_price"], 3.3)


class ChatPageTests(TestCase):
    def test_chat_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inventory Agent")
