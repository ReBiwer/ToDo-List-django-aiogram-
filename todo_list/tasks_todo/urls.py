from adrf import routers
from django.urls import path

from tasks_todo.views import TaskAPI, TagAPI

app_name = "tasks_todo"

router = routers.DefaultRouter()
router.register(r'api/v1/tasks', TaskAPI, "tasks")
router.register(r'api/v1/tags', TagAPI, "tags")

urlpatterns = [

] + router.urls
