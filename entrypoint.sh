#!/bin/sh
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding catalog, loyalty, and demo notifications (idempotent)..."
python manage.py seed_csm

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

if [ -n "${ADMIN_PHONE:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  echo "==> Ensuring configured admin user exists..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()
phone = os.environ['ADMIN_PHONE']
password = os.environ['ADMIN_PASSWORD']
email = os.environ.get('ADMIN_EMAIL', 'admin@csmsilks.com')

user = User.objects.filter(phone=phone).first()
if user is None:
    User.objects.create_superuser(
        username=phone,
        phone=phone,
        email=email,
        password=password,
    )
    print(f'Admin user created with phone {phone}')
else:
    updates = []
    if not user.is_staff:
        user.is_staff = True
        updates.append('is_staff')
    if not user.is_superuser:
        user.is_superuser = True
        updates.append('is_superuser')
    if email and user.email != email:
        user.email = email
        updates.append('email')
    user.set_password(password)
    updates.append('password')
    user.save(update_fields=updates)
    print(f'Admin user updated for phone {phone}')
"
else
  echo "==> Skipping admin bootstrap; set ADMIN_PHONE and ADMIN_PASSWORD to enable it."
fi

echo "==> Starting Gunicorn..."
exec gunicorn csm_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class sync \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level ${LOG_LEVEL:-info} \
    --forwarded-allow-ips="*"
