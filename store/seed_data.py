"""
Simple data seeder for the Store app.
Run with:  python manage.py shell < store/seed_data.py
"""

from decimal import Decimal
from datetime import date
from store.models import (
    Promotion,
    Collection,
    Product,
    Customer,
    Order,
    OrderItems,
    Address,
    Cart,
    CartItem,
)

# ---------- Clear existing data (optional) ----------
OrderItems.objects.all().delete()
Order.objects.all().delete()
CartItem.objects.all().delete()
Cart.objects.all().delete()
Address.objects.all().delete()
Product.promotions.through.objects.all()
Product.objects.all().delete()
Collection.objects.all().delete()
Promotion.objects.all().delete()
Customer.objects.all().delete()

# ---------- Promotions ----------
promo10 = Promotion.objects.create(description="10% Off", discount=0.10)
promo20 = Promotion.objects.create(description="20% Off", discount=0.20)

# ---------- Collections ----------
summer = Collection.objects.create(title="Summer Collection")
winter = Collection.objects.create(title="Winter Collection")

# ---------- Products ----------
p1 = Product.objects.create(
    title="T-Shirt",
    slug="t-shirt",
    description="Cotton T-shirt",
    unit_price=Decimal("19.99"),
    inventory=100,
    collection=summer,
)
p2 = Product.objects.create(
    title="Jacket",
    slug="jacket",
    description="Warm winter jacket",
    unit_price=Decimal("79.99"),
    inventory=50,
    collection=winter,
)
p1.promotions.add(promo10)
p2.promotions.add(promo20)

# Feature a product in a collection
summer.featured_product = p1
summer.save()
winter.featured_product = p2
winter.save()

# ---------- Customers ----------
alice = Customer.objects.create(
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com",
    phone="1234567890",
    birth_date=date(1990, 5, 17),
    membership=Customer.MEMBERSHIP_GOLD,
)
bob = Customer.objects.create(
    first_name="Bob",
    last_name="Brown",
    email="bob@example.com",
    phone="0987654321",
    birth_date=date(1985, 8, 23),
    membership=Customer.MEMBERSHIP_SILVER,
)

# ---------- Addresses ----------
Address.objects.create(street="123 Main St", city="Cairo", customer=alice)
Address.objects.create(street="456 Nile Ave", city="Giza", customer=bob)

# ---------- Orders & Items ----------
order1 = Order.objects.create(customer=alice, payment_status=Order.PAYMENT_COMPLETE)
OrderItems.objects.create(
    order=order1, product=p1, quantity=2, unit_price=p1.unit_price
)

order2 = Order.objects.create(customer=bob, payment_status=Order.PAYMENT_PENDING)
OrderItems.objects.create(
    order=order2, product=p2, quantity=1, unit_price=p2.unit_price
)

# ---------- Carts ----------
cart1 = Cart.objects.create()
CartItem.objects.create(cart=cart1, product=p1, quantity=3)
CartItem.objects.create(cart=cart1, product=p2, quantity=1)

print("✅ Seeding completed.")
