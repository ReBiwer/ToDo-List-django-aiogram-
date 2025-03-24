from adrf.serializers import ModelSerializer, Serializer
from adrf.generics import aget_object_or_404
from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.transaction import Atomic
from rest_framework import serializers

from tasks_todo.models import Tag, Task


class AsyncAtomicContextManager(Atomic):
    def __init__(self, using=None, savepoint=True, durable=False):
        super().__init__(using, savepoint, durable)

    async def __aenter__(self):
        await sync_to_async(super().__enter__)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await sync_to_async(super().__exit__)(exc_type, exc_value, traceback)


class TagSerializer(ModelSerializer):
    pk_tag: str = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["pk_tag","name"]
        read_only_fields = ["pk_tag"]

    def get_pk_tag(self, obj: Tag) -> str:
        return f"{obj.name}_pk"


class TaskSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Task
        fields = ["pk_task", "tg_id", "title", "created_at", "description", "date_end", "tags"]
        read_only_fields = ["pk_task"]

    async def acreate(self, validated_data):
        tags_data = validated_data.pop("tags")
        async with AsyncAtomicContextManager():
            task, _ = await Task.objects.aget_or_create(**validated_data)
            for tag in tags_data:
                tag, _ = await Tag.objects.aget_or_create(name=tag["name"])
                await sync_to_async(task.tags.add)(tag)
            return task
