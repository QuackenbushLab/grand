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

`pip: django django-widget-tweaks gunicorn psycopg2-binary djangorestframework-datatables djangorestframework django-filter`

`pandas sklearn requests statsmodels`

`apt: python3-pip python3-dev libpq-dev postgresql-contrib nginx curl`

Firewall

`sudo ufw allow 8000`

Launch server

`python3 manage.py runserver 0.0.0.0:8000`

Deployment:

SCP transfer

`scp -r -i /Volumes/home$/mab8354/Misc/amazonKey/Virginia.pem granddb/ ubuntu@34.207.196.182:`

`chmod -R 755 granddb`

`sudo -H pip3 install virtualenv`

`virtualenv venv`

`source venv/bin/activate`

/!\ inside venv

`pip3 install django gunicorn psycopg2-binary pillow`

Settings

`change API address in template`

`nano settings.py`

`ALLOWED_HOSTS = [ip,]`

`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`

Django

`sudo ufw allow 8000`

Gunicorn


paste `sudo nano /etc/systemd/system/gunicorn.socket`

paste `sudo nano /etc/systemd/system/gunicorn.service`

`sudo systemctl start gunicorn.socket`

`sudo systemctl enable gunicorn.socket`

`sudo systemctl status gunicorn.socket`

`sudo systemctl daemon-reload`

`sudo systemctl restart gunicorn`

Nginx

`debug=FALSE` in settings

paste in `nano /etc/nginx/sites-available/granddb`

`sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled`

sudo nginx -t

sudo systemctl restart nginx

sudo systemctl restart gunicorn

sudo ufw allow 'Nginx Full'



