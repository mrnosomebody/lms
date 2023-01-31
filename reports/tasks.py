from lms.celery import app
from reports.models import Report
from reports.utils import get_data, write_to_excel


@app.task
def generate_report():
    report = Report.objects.create()

    # uncomment for testing get_task_status()
    # time.sleep(20)

    data = get_data()

    file = write_to_excel(data['specialties_data'], data['study_groups_data'])

    if file:
        report.file = file
        report.status = 'completed'
        report.save()
    else:
        report.status = 'failed'
        report.save()
