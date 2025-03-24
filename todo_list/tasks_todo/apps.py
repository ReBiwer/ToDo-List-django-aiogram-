from django.apps import AppConfig


class TasksTodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_todo'

    def ready(self):
        import tasks_todo.signals
