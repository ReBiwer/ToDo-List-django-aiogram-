from adrf.serializers import ModelSerializer, Serializer
from asgiref.sync import sync_to_async
from rest_framework import serializers

from tasks_todo.models import Tag, Task
from tasks_todo.utils import AsyncAtomicContextManager


class TagSerializer(ModelSerializer):
    pk_tag: str = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["pk_tag","name"]

    def get_pk_tag(self, obj: Tag) -> str:
        return f"{obj.name}_pk"


class TaskSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Task
        fields = ["pk_task", "tg_id", "title", "created_at", "description", "date_end", "tags"]
        read_only_fields = ["pk_task", "created_at"]

    async def acreate(self, validated_data):
        tags_data = validated_data.pop("tags")
        async with AsyncAtomicContextManager():
            task, _ = await Task.objects.aget_or_create(**validated_data)
            for tag in tags_data:
                tag, _ = await Tag.objects.aget_or_create(name=tag["name"])
                await sync_to_async(task.tags.add)(tag)
            return task
