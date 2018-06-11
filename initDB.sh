#!/bin/sh 

rm -rf db.sqlite3
rm -rf snuariapi/migrations
python manage.py makemigrations snuariapi
python manage.py migrate
