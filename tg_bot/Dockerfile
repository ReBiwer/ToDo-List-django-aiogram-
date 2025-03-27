FROM python:3.12

WORKDIR /bot

COPY requirements.txt bot/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r bot/requirements.txt

COPY ./tg_bot/ /bot
CMD ["python", "tg_bot/run_bot.py"]
