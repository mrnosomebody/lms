from rest_framework.viewsets import ModelViewSet

from api.models import Curator, Student, Discipline, StudyGroup, Specialty
from api.permissions import CreateOrOwnerPermission
from api.serializers import (
    CuratorSerializer,
    StudentSerializer,
    DisciplineSerializer,
    StudyGroupSerializer,
    SpecialtySerializer
)


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    permission_classes = (CreateOrOwnerPermission,)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (CreateOrOwnerPermission,)


class DisciplineViewSet(ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
