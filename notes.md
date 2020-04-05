Creation date of GRAND October 1st 2019 at 8:37:39pm

Update to github is:

1. Transfer .csv files

` scp -r -i /Users/mab8354/Virginia.pem granddb/*.csv ubuntu@54.80.24.97:~/granddb/`

2. set debug to false

3. change API adress in tempaltes

4. change API address in help page redoc

and create db sqlite3 in the server.

run the server through

`python3 manage.py runserver`

import new db

`python3 load_data.py`

Requires

/!\ inside and outside venv

`pip3 install django django-widget-tweaks djangorestframework-datatables djangorestframework django-filter`

`pip3 install -U drf-yasg`

`pip3 install scipy pandas sklearn requests statsmodels`

`apt: python3-pip python3-dev libpq-dev postgresql-contrib nginx curl`

Firewall

`sudo ufw allow 8000`

to block port

`sudo ufw delete allow 8000`

Launch server

`python3 manage.py runserver 0.0.0.0:8000`

Deployment:

SCP transfer

`scp -r -i /Volumes/home$/mab8354/Misc/amazonKey/Virginia.pem granddb/ ubuntu@54.80.24.97:`

`chmod -R 755 granddb`

`sudo -H pip3 install virtualenv`

`virtualenv venv`

`source venv/bin/activate`

/!\ inside venv only

`pip3 install django gunicorn psycopg2-binary pillow`

To exit venv `deactivate`

Settings

`change API address in template`

`nano settings.py`

`ALLOWED_HOSTS = [ip,grand.tm4.org,www.grand.tm4.org]`

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

paste in `sudo nano /etc/nginx/sites-available/granddb`

`sudo ln -s /etc/nginx/sites-available/granddb /etc/nginx/sites-enabled`

sudo nginx -t

sudo systemctl restart nginx

sudo systemctl restart gunicorn

sudo ufw allow 'Nginx Full'



