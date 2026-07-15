from datetime import date

from celery_worker import celery
from controllers.models import Student, Company, Drive, Application


@celery.task(name="tasks.daily_placement_summary")
def daily_placement_summary():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    active_drives = Drive.query.filter(
        Drive.status == "Approved",
        Drive.deadline_date >= date.today()
    ).count()

    summary = {
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "active_drives": active_drives,
        "total_applications": total_applications
    }

    print("Daily Placement Summary")
    print(summary)

    return summary