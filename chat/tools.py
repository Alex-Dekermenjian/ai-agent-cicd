from decimal import Decimal
from .models import Item


def check_stock(name):
    """Look up how many of an item we have and its price."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
    }


def list_items():
    """Return every item in the inventory."""
    items = Item.objects.all()

    return {
        "items": [
            {
                "name": i.name,
                "quantity": i.quantity,
                "price": float(i.price),
            }
            for i in items
        ]
    }


def add_item(name, quantity, price=0):
    """Create a new item, or add to an existing item's stock."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is not None:
        item.quantity += quantity
        item.price = price
        item.save()

        return {
            "name": item.name,
            "quantity": item.quantity,
            "price": float(item.price),
            "created": False,
        }

    item = Item.objects.create(
        name=name,
        quantity=quantity,
        price=price,
    )

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
        "created": True,
    }


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
            "price": float(item.price),
        }

    item.quantity -= quantity
    item.save()

    return {
        "name": item.name,
        "quantity": item.quantity,
        "price": float(item.price),
    }


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    item.delete()

    return {
        "deleted": name,
    }


def change_price_percent(name, percent):
    """Increase or decrease an item's price by a percentage."""
    item = Item.objects.filter(name__iexact=name).first()

    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    old_price = item.price

    multiplier = Decimal("1") + Decimal(str(percent)) / Decimal("100")

    item.price = old_price * multiplier
    item.save()

    return {
        "name": item.name,
        "old_price": float(old_price),
        "percent_change": percent,
        "new_price": float(item.price),
    }


TOOL_DECLARATIONS = [
    {
        "type": "function",
        "name": "check_stock",
        "description": "Look up the current quantity and price of a single item in the inventory.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item.",
                },
            },
            "required": ["name"],
        },
    },

    {
        "type": "function",
        "name": "list_items",
        "description": "Return every item in the inventory with quantity and price.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },

    {
        "type": "function",
        "name": "add_item",
        "description": "Add stock to the inventory. If the item exists, increase its quantity and update its price.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to add.",
                },
                "price": {
                    "type": "number",
                    "description": "The unit price of the item.",
                },
            },
            "required": ["name", "quantity", "price"],
        },
    },

    {
        "type": "function",
        "name": "remove_stock",
        "description": "Reduce the quantity of an existing item.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to remove.",
                },
            },
            "required": ["name", "quantity"],
        },
    },

    {
        "type": "function",
        "name": "delete_item",
        "description": "Permanently remove an item from the inventory.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item.",
                },
            },
            "required": ["name"],
        },
    },

    {
        "type": "function",
        "name": "change_price_percent",
        "description": "Increase or decrease the unit price of an inventory item by a percentage.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the inventory item.",
                },
                "percent": {
                    "type": "number",
                    "description": "Percentage change. Example: 50 means increase by 50 percent, -20 means decrease by 20 percent.",
                },
            },
            "required": ["name", "percent"],
        },
    },
]


TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
    "change_price_percent": change_price_percent,
}