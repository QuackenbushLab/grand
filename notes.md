Creation date of GRAND October 1st 2019 at 8:37:39pm

Disks:
Follow this guide for mounting:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html

Disks specs:
Disk /dev/xvdd: 1000 GiB
Adipose_Subcutaneous_AllSamples.csv -> Brain_Other_AllSamples.csv 
Disk /dev/xvdb: 1000 GiB
Breast_AllSamples.csv -> Pituitary_AllSamples.csv (923)
Disk /dev/xvdc: 1000 GiB
Skeletal_Muscle_AllSamples.csv-> Whole_Blood_AllSample.csv (849)

AWS is :
/usr/local/bin/aws

Update to github is:

1. Transfer .csv files

- mysql database
` scp -r -i /Users/mab8354/Virginia.pem granddb/db.sqlite3 ubuntu@34.207.177.160:~/granddb/`

- data folder
` scp -r -i /Users/mab8354/Virginia.pem granddb/data/*.csv ubuntu@34.207.177.160:~/granddb/data/`

- molcluereg folder (can be skipped if no major changes)

` scp -r -i /Users/mab8354/Virginia.pem granddb/static/molcluereg/ ubuntu@34.207.177.160:~/granddb/static/`

- static/data folder

` scp -r -i /Users/mab8354/Virginia.pem granddb/static/data/*.csv ubuntu@34.207.177.160:~/granddb/static/data/`

- static/js folder

` scp -r -i /Users/mab8354/Virginia.pem granddb/static/js/ ubuntu@34.207.177.160:~/granddb/static/`

2. set debug to false

3. change API adress in templates

4. change API address in help page redoc

and create db sqlite3 in the server.

run the server through

`python3 manage.py runserver`

import new db

`python3 load_data.py`

Requires

/!\ inside and outside venv

`python -m pip install "dask[complete]" `

`pip install boto3`

`pip3 install django django-widget-tweaks djangorestframework-datatables djangorestframework django-filter`

`pip3 install -U drf-yasg`

`pip3 install scipy pandas sklearn requests statsmodels`

` /home/ubuntu/venv/bin/python3 -m pip install mygene`

`apt: python3-pip python3-dev libpq-dev postgresql-contrib nginx curl`

Firewall

`sudo ufw allow 8000`

to block port

`sudo ufw delete allow 8000`

Launch server

`python3 manage.py runserver 0.0.0.0:8000`

Deployment:

/!\ Important local settings is on disk only, no github

SCP transfer

`scp -r -i /Volumes/home$/mab8354/Misc/amazonKey/Virginia.pem granddb/ ubuntu@34.207.177.160:`

`chmod -R 755 granddb`

`sudo -H pip3 install virtualenv`

`virtualenv venv38 --python=/usr/bin/python3.8`

`source venv38/bin/activate`

/!\ inside venv only

`pip3 install django gunicorn psycopg2-binary pillow`
`python -m pip install "dask[complete]" `
`pip install boto3`

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

**Nginx

`debug=FALSE` in settings

paste in `sudo nano /etc/nginx/sites-available/granddb` (and change IP address here)

`sudo ln -s /etc/nginx/sites-available/granddb /etc/nginx/sites-enabled`

allow file uploads up to 500 mb

sudo nano /etc/nginx/nginx.conf

sudo nginx -t

sudo systemctl restart nginx

sudo systemctl restart gunicorn

sudo ufw allow 'Nginx Full'



Don't forget 
`python3 manage.py collectstatic`

- Add static root in `settings.py`

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Then `python3 manage.py collectstatic`


EMAIL:

- Unlock captcha

- enable less secure apps

https://stackoverflow.com/questions/20337040/getting-error-while-sending-email-through-gmail-smtp-please-log-in-via-your-w
