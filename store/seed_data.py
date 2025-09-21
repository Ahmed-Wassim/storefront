"""
Seed the Store app with random data using Faker.

Usage:
    python manage.py shell < store/seed_data.py
    # or pass numbers as environment variables, e.g.:
    PRODUCTS=20 CUSTOMERS=15 ORDERS=10 python manage.py shell < store/seed_data.py
"""

import os
import random
from decimal import Decimal
from faker import Faker
from datetime import timedelta
from django.utils import timezone

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

fake = Faker()

# ---------- CONFIG (read from environment or default) ----------
NUM_PRODUCTS = int(os.getenv("PRODUCTS", 10))
NUM_CUSTOMERS = int(os.getenv("CUSTOMERS", 10))
NUM_ORDERS = int(os.getenv("ORDERS", 10))
NUM_CARTS = int(os.getenv("CARTS", 5))

# ---------- OPTIONAL: Clear old data ----------
print("Clearing old data…")
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
promos = [
    Promotion.objects.create(description=f"{p}% off", discount=p / 100)
    for p in (5, 10, 15, 20)
]

# ---------- Collections ----------
collections = [
    Collection.objects.create(title=fake.word().capitalize()) for _ in range(5)
]

# ---------- Products ----------
products = []
for _ in range(NUM_PRODUCTS):
    c = random.choice(collections)
    p = Product.objects.create(
        title=fake.word().capitalize(),
        slug=fake.slug(),
        description=fake.text(50),
        unit_price=Decimal(random.randint(5, 100)),
        inventory=random.randint(1, 200),
        collection=c,
    )
    # Add random promotions
    p.promotions.add(*random.sample(promos, k=random.randint(0, len(promos))))
    products.append(p)

# Feature a product in each collection
for col in collections:
    col.featured_product = random.choice(products)
    col.save()

# ---------- Customers ----------
customers = []
for _ in range(NUM_CUSTOMERS):
    customers.append(
        Customer.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.msisdn()[:13],
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
            membership=random.choice(
                [
                    Customer.MEMBERSHIP_BRONZE,
                    Customer.MEMBERSHIP_SILVER,
                    Customer.MEMBERSHIP_GOLD,
                ]
            ),
        )
    )

# ---------- Addresses ----------
for cust in customers:
    for _ in range(random.randint(1, 2)):
        Address.objects.create(
            street=fake.street_address(), city=fake.city(), customer=cust
        )

# ---------- Orders & Items ----------
orders = []
for _ in range(NUM_ORDERS):
    cust = random.choice(customers)
    order = Order.objects.create(
        customer=cust,
        payment_status=random.choice(
            [
                Order.PAYMENT_PENDING,
                Order.PAYMENT_COMPLETE,
                Order.PAYMENT_FAILED,
            ]
        ),
        placed_at=timezone.now() - timedelta(days=random.randint(0, 90)),
    )
    # add 1-3 products to each order
    for _ in range(random.randint(1, 3)):
        prod = random.choice(products)
        OrderItems.objects.create(
            order=order,
            product=prod,
            quantity=random.randint(1, 5),
            unit_price=prod.unit_price,
        )
    orders.append(order)

# ---------- Carts ----------
for _ in range(NUM_CARTS):
    cart = Cart.objects.create()
    for _ in range(random.randint(1, 4)):
        prod = random.choice(products)
        CartItem.objects.create(cart=cart, product=prod, quantity=random.randint(1, 5))

print("✅ Seeding completed.")
print(
    f"Created: {len(products)} products, {len(customers)} customers, "
    f"{len(orders)} orders, {NUM_CARTS} carts."
)
