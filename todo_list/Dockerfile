FROM python:3.12

WORKDIR /app

COPY requirements.txt app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt

COPY ./todo_list/ /app
CMD ["python", "todo_list/manage.py", "runserver", "0.0.0.0:8000"]
