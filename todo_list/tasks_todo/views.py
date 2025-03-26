from adrf.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from tasks_todo.models import Task, Tag
from tasks_todo.serializers import TaskSerializer, TagSerializer


class TaskAPI(ModelViewSet):
    queryset = Task.objects.prefetch_related("tags").all()
    serializer_class = TaskSerializer


    @extend_schema(operation_id="task_v1_aretrive")
    async def aretrieve(self, request, *args, **kwargs):
        return await super().aretrieve(request, *args, **kwargs)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tg_id',
                location=OpenApiParameter.QUERY,
                description='ID пользователя в телеграмм',
                required=True,
                type=int
            ),
        ]
    )
    async def alist(self, tg_id: int, *args, **kwargs):
        tg_id = self.request.query_params["tg_id"]
        self.queryset = Task.objects.filter(tg_id=tg_id).all()
        return await super().alist(*args, **kwargs)


class TagAPI(ModelViewSet):
    queryset = Tag.objects.prefetch_related("tasks").all()
    serializer_class = TagSerializer
    lookup_field = "pk_tag"


    @extend_schema(operation_id="tag_v1_aretrive")
    async def aretrieve(self, request, *args, **kwargs):
        return await super().aretrieve(request, *args, **kwargs)
