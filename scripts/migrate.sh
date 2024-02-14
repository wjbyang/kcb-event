rm db.sqlite3
rm -r eventScheduler/migrations
python manage.py makemigrations eventScheduler
python manage.py migrate eventScheduler
python manage.py makemigrations
python manage.py migrate