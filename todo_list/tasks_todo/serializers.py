from adrf.serializers import ModelSerializer
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

    async def aupdate(self, instance: Task, validated_data):
        tags_data = validated_data.pop("tags")
        async with AsyncAtomicContextManager():
            # Обновление полей задачи
            instance.title = validated_data.get("title")
            instance.description = validated_data.get("description")
            instance.date_end = validated_data.get("date_end")
            await instance.asave()

            # Текущие теги
            current_tags = {tag.name: tag for tag in instance.tags.all()}
            requested_tags = set()

            # Обработка элементов
            for tag_data in tags_data:
                tag_name = tag_data.get('tag_name')

                # Проверка наличия тега
                if tag_name and tag_name in current_tags:
                    requested_tags.add(tag_name)

                # Создание нового тега
                else:
                    new_tag, _ = await Tag.objects.aget_or_create(name=tag_data["name"])
                    await sync_to_async(instance.tags.add)(new_tag)

            # Удаление отсутствующих в запросе элементов
            for tag_name, tag in current_tags.items():
                if tag_name not in requested_tags:
                    await sync_to_async(instance.tags.remove)(tag)
        return instance
