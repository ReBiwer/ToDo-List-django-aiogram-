from adrf.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from tasks_todo.models import Task, Tag
from tasks_todo.serializers import TaskSerializer, TagSerializer


class TaskAPI(ModelViewSet):
    queryset = Task.objects.prefetch_related("tags").all()
    serializer_class = TaskSerializer

class TagAPI(ModelViewSet):
    queryset = Tag.objects.prefetch_related("tasks").all()
    serializer_class = TagSerializer
    lookup_field = "pk_tag"
