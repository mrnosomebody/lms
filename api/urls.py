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

urlpatterns = router.urls
