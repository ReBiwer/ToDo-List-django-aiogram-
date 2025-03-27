#!/bin/bash
# Запуск Django
python todo_list/manage.py runserver 0.0.0.0:8000 &&

# Запуск Celery
cd todo_list && celery -A todo_list worker --loglevel=info
