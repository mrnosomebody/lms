from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import (
    Curator,
    Student,
    Discipline,
    StudyGroup,
    Specialty
)
from api.serializers import (
    CuratorSerializer,
    StudentSerializer,
    DisciplineSerializer,
    StudyGroupSerializer,
    SpecialtySerializer
)
from api.permissions import CreateOrOwnerPermission


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    permission_classes = (CreateOrOwnerPermission,)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('group')
    serializer_class = StudentSerializer
    permission_classes = (CreateOrOwnerPermission,)


class DisciplineViewSet(ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.select_related('specialty')
    serializer_class = StudyGroupSerializer


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.select_related('curator').prefetch_related('disciplines')
    serializer_class = SpecialtySerializer

    @action(methods=['PATCH', 'DELETE'], detail=True)
    def update_specialty(self, request, pk=None):
        serializer = SpecialtySerializer(
            self.get_object(),
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
