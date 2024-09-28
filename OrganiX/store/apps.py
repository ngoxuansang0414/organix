from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = "store"

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from store.tasks import my_scheduled_task

        if not PeriodicTask.objects.filter(name="My Scheduled Task").exists():
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=2,
                period=IntervalSchedule.MINUTES,
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name="My Scheduled Task",
                task="store.tasks.my_scheduled_task",
            )
