#!/bin/bash

# Build the project
echo "Building the project..."
python -m pip install -r requirements.txt

echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating or updating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); u.set_password('admin123'); u.is_staff = True; u.is_superuser = True; u.save(); print('Superuser admin ready!')"

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

