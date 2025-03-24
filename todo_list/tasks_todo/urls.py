from adrf import routers
from django.urls import path, include

from tasks_todo.views import TaskAPI

app_name = "tasks_todo"

router = routers.DefaultRouter()
router.register(r'tasks', TaskAPI, basename="api_task")

urlpatterns = [
    path("api/v1/", include(router.urls), name="api_task"),
]
