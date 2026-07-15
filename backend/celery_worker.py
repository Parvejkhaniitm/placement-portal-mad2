from celery import Celery
from celery.schedules import crontab


from app import app



def make_celery(flask_app):
    celery = Celery(
        flask_app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    celery.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=False
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)

celery.conf.beat_schedule = {
    "daily-placement-summary": {
        "task": "tasks.daily_placement_summary",
        "schedule": crontab(hour=9, minute=0)
    }
}
import tasks 