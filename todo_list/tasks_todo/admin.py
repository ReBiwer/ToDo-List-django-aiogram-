from django.contrib import admin
from .models import Task, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["pk_task", "tg_id", "title", "created_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["pk_tag", "name"]
