# CSM-Silks-Ecom-Backend

Django + Django REST Framework backend for the CSM Silks ecommerce platform.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_csm
python manage.py runserver 0.0.0.0:8000
```

## Core accounts

- Admin: `admin@csmsilks.com` / `admin123`
- Customer OTP phone: `+918888888888`

## Useful commands

```bash
python manage.py check
python manage.py test accounts catalog cart orders payments inventory loyalty notifications analytics shipping reviews ai
```

## API

- Health: `/health` and `/api/health`
- Docs: `/api/docs`
- Customer APIs: `/api/products`, `/api/search`, `/api/cart`, `/api/orders`
- Admin APIs: `/api/admin/dashboard`, `/api/admin/products`, `/api/admin/orders`
