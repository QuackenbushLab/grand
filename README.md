run the server through

`python3 manage.py runserver`

import new db

`python3 manage.py load_cell_data`

`python3 manage.py load_drug_data`

make migration

`python3 manage makemigrations`

run migration

`python3 manage.py migrate`

Requires

`pip: django django-widget-tweaks gunicorn psycopg2-binary djangorestframework-datatables djangorestframework`

`apt: python3-pip python3-dev libpq-dev postgresql-contrib nginx curl`

Firewall

`sudo ufw allow 8000`

Launch server

`python3 manage.py runserver 0.0.0.0:8000`
