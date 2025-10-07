from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
import random
from django.contrib.auth import get_user_model
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

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the store with fake data using Faker"

    def handle(self, *args, **options):
        fake = Faker()
        fake.unique.clear()

        self.stdout.write(self.style.WARNING("🧹 Clearing old data..."))
        OrderItems.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Promotion.objects.all().delete()
        Collection.objects.all().delete()
        Customer.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ Creating collections..."))
        collections = [Collection.objects.create(title=fake.word()) for _ in range(5)]

        self.stdout.write(self.style.SUCCESS("✅ Creating promotions..."))
        promotions = [
            Promotion.objects.create(
                description=fake.sentence(), discount=random.uniform(0.05, 0.5)
            )
            for _ in range(5)
        ]

        self.stdout.write(self.style.SUCCESS("✅ Creating products..."))
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
            product.promotions.set(
                random.sample(promotions, random.randint(0, len(promotions)))
            )
            products.append(product)

        self.stdout.write(self.style.SUCCESS("✅ Creating customers..."))
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
                continue

        self.stdout.write(self.style.SUCCESS("✅ Creating carts and cart items..."))
        carts = []
        for _ in range(5):
            cart = Cart.objects.create()
            carts.append(cart)
            for product in random.sample(products, random.randint(1, 3)):
                CartItem.objects.create(
                    cart=cart, product=product, quantity=random.randint(1, 5)
                )

        self.stdout.write(self.style.SUCCESS("✅ Creating orders and order items..."))
        orders = []
        if customers and products:
            for _ in range(10):
                customer = random.choice(customers)
                order = Order.objects.create(customer=customer)
                orders.append(order)
                for prod in random.sample(products, random.randint(1, 3)):
                    OrderItems.objects.create(
                        order=order,
                        product=prod,
                        quantity=random.randint(1, 5),
                        unit_price=prod.unit_price,
                    )

        self.stdout.write(self.style.SUCCESS("🎉 Seeding completed successfully!"))
        self.stdout.write(
            f"Created: {len(collections)} collections, {len(promotions)} promotions, "
            f"{len(products)} products, {len(customers)} customers, {len(orders)} orders, {len(carts)} carts."
        )
