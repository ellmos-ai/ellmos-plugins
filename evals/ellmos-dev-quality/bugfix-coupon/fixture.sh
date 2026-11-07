#!/bin/sh
set -e
cat > pricing.py <<'PY'
def apply_discount(amount, percent):
    """Return amount reduced by percent (0-100), rounded to cents."""
    return round(amount * (1 - percent / 100), 2)
PY
cat > cart.py <<'PY'
from pricing import apply_discount


class Item:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity


def line_total(item, coupon_percent=0):
    unit_price = apply_discount(item.price, coupon_percent)
    return round(unit_price * item.quantity, 2)


def checkout(items, coupon_percent=0):
    subtotal = sum(line_total(item, coupon_percent) for item in items)
    return apply_discount(subtotal, coupon_percent)
PY
cat > test_cart.py <<'PY'
from cart import Item, checkout


def test_single_item_without_coupon():
    assert checkout([Item("book", 20.0)]) == 20.0
PY
