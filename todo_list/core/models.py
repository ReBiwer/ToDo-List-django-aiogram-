from django.db import models



class ProfileUser(models.Model):
    bio = models.TextField(max_length=250, verbose_name="О себе")
    telegram_id = models.IntegerField(verbose_name="ID пользователя в телеграмме")
