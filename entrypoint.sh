python ./core/manage.py makemigrations --noinput
python ./core/manage.py migrate --noinput
python ./core/manage.py runserver 0.0.0.0:8000
