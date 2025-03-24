from django.db import models
from django.utils import timezone


class Tag(models.Model):
    pk_tag = models.CharField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Тег")

    def save(self, *args, **kwargs):
        if not self.pk_tag:
            self.pk_tag = f"{self.name}_pk"
        super().save(*args, **kwargs)

class Task(models.Model):
    pk_task = models.CharField(primary_key=True)
    tg_id = models.IntegerField(verbose_name="ID пользователя в телеграмме")
    title = models.CharField(max_length=200, verbose_name="Заголовок задачи")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Время создания")
    description = models.TextField(max_length=350, verbose_name="Описание задачи")
    date_end = models.DateTimeField(verbose_name="Дата исполнения")

    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name="Теги")

    def save(self, *args, **kwargs):
        if not self.pk_task:
            self.pk_task = f"{self.tg_id}_{timezone.now()}"
        super().save(*args, **kwargs)
