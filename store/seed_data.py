import random
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from faker import Faker
from store.models import (
    Product,
    Collection,
    Promotion,
    Customer,
    Order,
    OrderItems,
    Cart,
    CartItem,
)

fake = Faker()
fake.unique.clear()  # Reset any previous uniqueness cache


def seed_data():
    print("🧹 Clearing old data...")
    Product.objects.all().delete()
    Collection.objects.all().delete()
    Promotion.objects.all().delete()
    Customer.objects.all().delete()
    Order.objects.all().delete()
    Cart.objects.all().delete()
    CartItem.objects.all().delete()

    print("✅ Creating collections...")
    collections = []
    for _ in range(5):
        collection = Collection.objects.create(title=fake.word())
        collections.append(collection)

    print("✅ Creating promotions...")
    promotions = []
    for _ in range(5):
        promo = Promotion.objects.create(
            description=fake.sentence(), discount=random.uniform(0.05, 0.5)
        )
        promotions.append(promo)

    print("✅ Creating products...")
    products = []
    for _ in range(15):
        product = Product.objects.create(
            title=fake.unique.word().capitalize(),
            slug=fake.unique.slug(),
            description=fake.text(max_nb_chars=200),
            unit_price=random.uniform(10.0, 500.0),
            inventory=random.randint(0, 100),
            collection=random.choice(collections),
        )
        # Assign random promotions
        product.promotions.set(
            random.sample(promotions, random.randint(0, len(promotions)))
        )
        products.append(product)

    print("✅ Creating customers...")
    customers = []
    for _ in range(10):
        try:
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="1234",
            )
            cust = Customer.objects.create(
                user=user,
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
            customers.append(cust)
        except IntegrityError:
            print("⚠️ Skipping duplicate customer.")
            continue

    print("✅ Creating carts and cart items...")
    carts = []
    for _ in range(5):
        cart = Cart.objects.create()
        carts.append(cart)

        # Add random unique products per cart
        products_in_cart = random.sample(products, random.randint(1, 3))
        for product in products_in_cart:
            CartItem.objects.create(
                cart=cart, product=product, quantity=random.randint(1, 5)
            )

    print("✅ Creating orders and order items...")
    orders = []
    if customers and products:
        for _ in range(10):
            customer = random.choice(customers)
            order = Order.objects.create(customer=customer)
            orders.append(order)

            # Random 1–3 items per order
            order_products = random.sample(products, random.randint(1, 3))
            for prod in order_products:
                OrderItems.objects.create(
                    order=order,
                    product=prod,
                    quantity=random.randint(1, 5),
                    unit_price=prod.unit_price,
                )
    else:
        print("⚠️ Skipping order creation — missing customers or products.")

    print("🎉 Seeding completed successfully!")
    print(
        f"Created: {len(collections)} collections, {len(promotions)} promotions, "
        f"{len(products)} products, {len(customers)} customers, {len(orders)} orders, {len(carts)} carts."
    )


if __name__ == "__main__":
    try:
        with transaction.atomic():
            seed_data()
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
