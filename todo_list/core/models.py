from django.db import models



class ProfileUser(models.Model):
    bio = models.TextField(max_length=250, verbose_name="О себе")
    tg_id = models.IntegerField(primary_key=True, verbose_name="ID пользователя в телеграмме")
