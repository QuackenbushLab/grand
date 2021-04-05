# Multiple File Upload

Example used in the blog post [Django Multiple Files Upload Using Ajax](https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html)

## Running Locally

```bash
git clone https://github.com/sibtc/multiple-file-upload.git

https://github.com/thalesbruno/django_bootstrap

https://github.com/sibtc/simple-file-upload.git

Following https://stackoverflow.com/questions/61711710/runtimeerror-class-not-set-defining-abstractbaseuser-as-class-django-co
for fixing the initial error
```

```bash
virtualenv -p python3 venv
```

```bash
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

```bash
python3 manage.py migrate
```

```bash
python3 manage.py runserver
```