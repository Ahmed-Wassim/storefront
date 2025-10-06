# 🏪 Django Store API

A modular **Django REST Framework** store application built with **JWT authentication** using Djoser.
The project demonstrates scalable architecture, clean RESTful design, and advanced Django features such as filters, permissions, and custom admin dashboards — all managed using **Pipenv**.

---

## 🚀 Features

* **Modular app structure**

  * `store` app – core e-commerce logic (products, collections, carts, customers, orders)
  * `tags` app – generic tagging system using Django content types
  * `core` app – integration layer, shared configurations, and utilities
* **JWT Authentication** with Djoser for secure login and registration
* **Nested routes** for related resources (e.g., `/store/collections/{id}/products/`)
* **Custom Admin Dashboard** featuring:

  * Inline order item editing
  * Product inventory management actions
  * Annotated product counts with clickable links
* **Django Filters** for advanced data querying
* **Role-based permissions** for secure access control
* **Generic relationships** for flexible tagging
* **UUID-based cart system** for unique and scalable cart handling
* Follows Django and REST API best practices

---

## 🧩 Project Structure

```
project_root/
│
├── core/                 # Core integration and global settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                # E-commerce logic
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py          # Custom admin dashboards
│
├── tags/                 # Generic tagging system
│   ├── models.py
│   └── admin.py
│
├── Pipfile
├── Pipfile.lock
└── manage.py
```

---

## 🛠️ Technologies Used

* **Python 3.12+**
* **Django 5+**
* **Django REST Framework**
* **Djoser** for JWT authentication
* **Django Filter**
* **Pipenv** for environment and dependency management
* **SQLite / PostgreSQL** (configurable)
* **UUID-based cart identifiers**

---

## ⚙️ Installation & Setup (Using Pipenv)

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/django-store.git
   cd django-store
   ```

2. **Install dependencies**

   ```bash
   pipenv install
   ```

3. **Activate the Pipenv shell**

   ```bash
   pipenv shell
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## 🔑 Authentication

Authentication is handled using **JWT tokens** via **Djoser**.

Example endpoints:

* `POST /auth/jwt/create/` – Obtain access and refresh tokens
* `POST /auth/jwt/refresh/` – Refresh access token
* `POST /auth/users/` – Register a new user

---

## 🧾 Example API Endpoints

| Resource    | Endpoint              | Method     | Description                      |
| ----------- | --------------------- | ---------- | -------------------------------- |
| Products    | `/store/products/`    | GET / POST | List or create products          |
| Collections | `/store/collections/` | GET / POST | Manage product collections       |
| Carts       | `/store/carts/`       | GET / POST | Manage shopping carts            |
| Customers   | `/store/customers/`   | GET / PUT  | Retrieve or update customer info |
| Orders      | `/store/orders/`      | GET / POST | Manage customer orders           |
| Tags        | `/tags/`              | GET / POST | Manage generic tags              |

---

## 🧱 Admin Dashboard Highlights

* Custom product admin with prepopulated slugs and inline editable pricing
* Product inventory bulk actions (e.g., clear inventory)
* Annotated collection view showing product counts with clickable links
* Inline order items management within orders
* Optimized queries and filters for admin efficiency

---

## 🧰 Permissions and Filters

* **Custom permissions** restrict access for certain operations such as order updates or product modifications.
* **Django Filter** enables powerful query customization, for example:

  ```
  /store/products/?collection_id=2&min_price=10&max_price=100
  ```

---

## 🧾 License

This project is licensed under the **MIT License** – see the LICENSE file for details.

---
