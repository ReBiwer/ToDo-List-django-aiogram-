from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from .tasks import notification_start_task
from django.utils import timezone

@receiver(post_save, sender=Task)
def schedule_notification(sender, instance: Task, **kwargs):
    msg_notify = (f"Настало время исполнения задания\n"
                  f"{instance.title}\n"
                  f"{instance.description}")
    time_notify = timezone.now() - instance.date_end
    notification_start_task.apply_async(
        args=[msg_notify, instance.tg_id],
        eta=time_notify,
    )