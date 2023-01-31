from django.urls import path
from rest_framework.routers import DefaultRouter

from reports.views import ReportViewSet, get_report, get_task_status

router = DefaultRouter()

router.register('reports', ReportViewSet)

urlpatterns = [
    path('reports/<int:id>/', get_report),
    path('tasks/<str:uuid>/', get_task_status)
]

urlpatterns += router.urls
