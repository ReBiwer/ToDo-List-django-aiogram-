from adrf.viewsets import ModelViewSet

from tasks_todo.models import Task
from tasks_todo.serializers import TaskSerializer


class TaskAPI(ModelViewSet):
    queryset = Task.objects.prefetch_related("tags").all()
    serializer_class = TaskSerializer
