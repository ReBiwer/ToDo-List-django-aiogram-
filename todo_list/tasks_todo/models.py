from django.db import models

from core.models import ProfileUser


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тег")

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовое задачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    description = models.TextField(max_length=350, verbose_name="Описание задачи")
    date_end = models.DateTimeField(verbose_name="Дата исполнения")

    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name="Теги")
    profile = models.ForeignKey(
        ProfileUser,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Профиль пользователя"
    )
