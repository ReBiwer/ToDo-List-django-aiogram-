from django.db import models



class Profile(models.Model):
    bio = models.TextField(max_length=250, verbose_name="О себе")
    telegram_id = models.IntegerField(max_length=15, verbose_name="ID пользователя в телеграмме")
