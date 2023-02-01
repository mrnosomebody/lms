from celery.result import AsyncResult
from django.http import FileResponse
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from reports.models import Report
from reports.serializers import ReportSerializer
from reports.tasks import generate_report


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        task = generate_report.delay()
        return Response(data={
            'task_id': task.id
        })


@api_view(['GET'])
def get_task_status(request, uuid: str):
    return Response(data={'status': AsyncResult(uuid).status})


def get_report(request, id: int):
    report = Report.objects.get(id=id)
    file = report.file
    return FileResponse(file)
