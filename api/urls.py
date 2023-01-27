from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (
    CuratorViewSet,
    StudentViewSet,
    StudyGroupViewSet,
    DisciplineViewSet,
    SpecialtyViewSet,
)

router = DefaultRouter()

router.register('curators', CuratorViewSet)
router.register('students', StudentViewSet)
router.register('study-groups', StudyGroupViewSet)
router.register('disciplines', DisciplineViewSet)
router.register('specialties', SpecialtyViewSet)

urlpatterns = [
    # path(
    #     'specialties/<int:id>/add_disciplines/',
    #     SpecialtyManageDisciplinesViewSet.as_view(),
    #     name='add_disciplines'
    # ),
    # path(
    #     'specialties/<int:id>/remove_disciplines/',
    #     SpecialtyManageDisciplinesViewSet.as_view(),
    #     name='remove_disciplines'
    # )
]

urlpatterns += router.urls
