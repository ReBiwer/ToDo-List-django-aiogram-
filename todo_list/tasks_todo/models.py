from django.db import models
from django.utils import timezone


class Tag(models.Model):
    pk = models.CharField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Тег")

    def save(self, *args, **kwargs):
        self.pk = f"{self.name}_pk"
        super().save(*args, **kwargs)

class Task(models.Model):
    pk = models.CharField(primary_key=True)
    tg_id = models.IntegerField(verbose_name="ID пользователя в телеграмме")
    title = models.CharField(max_length=200, verbose_name="Заголовое задачи")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Время создания")
    description = models.TextField(max_length=350, verbose_name="Описание задачи")
    date_end = models.DateTimeField(verbose_name="Дата исполнения")

    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name="Теги")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = f"{self.tg_id}_{timezone.now()}"
        super().save(*args, **kwargs)
